import io
from logging import log, WARNING
from typing import List, Tuple, Union

import numpy as np
from PIL import Image

from odineye.maps_downloaders.maps_downloader import MapsDownloader
from odineye.url_downloader.url_downloader import UrlDownloader
from odineye.utils.coordinates_convertion import wgs84_to_pixels
from odineye.utils.image_utils import resize_image


class GoogleMapsDownloader(MapsDownloader):
    """A class for downloading map sections from Google Maps."""
    MIN_ZOOM = 0
    MAX_ZOOM = 22

    def __init__(self, download_threads: int = 8, default_style: str = "satellite"):
        """
        Initialize the GoogleMapsDownloader with URL downloader and map styles.

        :param download_threads: Number of threads for downloading tiles.
        :param default_style: Default map style if not specified.
        """
        self._validate_style(default_style)
        self._default_style = default_style
        self._url_downloader = UrlDownloader(download_threads)
        self._styles = {"satellite": "s", "roadmap": "m", "hybrid": "y"}
        self._provider_url = "http://mts0.googleapis.com/vt?lyrs={style}&x={x}&y={y}&z={zoom}"

    def download(
            self,
            north_latitude: float,
            west_longitude: float,
            south_latitude: float,
            east_longitude: float,
            zoom: int,
            map_style: str = None,
            image_format: str = "RGB",
            resize: Union[None, Tuple[int, int]] = None,
            return_type: Union[str] = "PIL",
    ) -> Union[Image.Image, np.ndarray, bytes]:
        """
        Download a Google Maps section given geographical coordinates, zoom level, and style.

        :param north_latitude: Northern latitude of the map section.
        :param west_longitude: Western longitude of the map section.
        :param south_latitude: Southern latitude of the map section.
        :param east_longitude: Eastern longitude of the map section.
        :param zoom: Zoom level.
        :param map_style: Map style. Supported styles are "satellite", "roadmap", and "hybrid".
        :param image_format: Image format. Supported formats are "RGB" and "RGBA".
        :param resize: New size of the map section is a tuple (width, height) or (None, height) or (None, width).
        If both are provided, the aspect ratio may be distorted. If only one is provided, the original aspect ratio is
        maintained. If None, the original size is used.
        :param return_type: The type of the returned object. Supported types are "PIL", "numpy", and "bytes".
        :return: The combined map section. It can be a PIL Image object, a NumPy array, or a byte object, depending
        on the return_type parameter.
        """
        super().validate(
            north_latitude, west_longitude, south_latitude, east_longitude, zoom, map_style, image_format, resize,
            return_type
        )
        assert (
                GoogleMapsDownloader.MIN_ZOOM <= zoom <= GoogleMapsDownloader.MAX_ZOOM
        ), f"Zoom level must be between 0 and {GoogleMapsDownloader.MAX_ZOOM} inclusive."

        if map_style is None:
            map_style = self._default_style

        map_tiles, zoom = self._get_map_tiles(
            north_latitude, west_longitude, south_latitude, east_longitude, zoom, map_style
        )
        map_image = self._merge_tiles(
            map_tiles,
            north_latitude,
            west_longitude,
            south_latitude,
            east_longitude,
            zoom,
        )

        return self._postprocess_image(map_image, image_format, resize, return_type)

    def _get_urls(
            self,
            north_latitude: float,
            west_longitude: float,
            south_latitude: float,
            east_longitude: float,
            zoom: int,
            style: str,
    ) -> List[str]:
        """
        Generate URLs for all tiles covering the specified area at the given zoom level and style.

        :param north_latitude: Northern latitude of the map section.
        :param west_longitude: Western longitude of the map section.
        :param south_latitude: Southern latitude of the map section.
        :param east_longitude: Eastern longitude of the map section.
        :param zoom: Zoom level.
        :param style: Map style.
        :return: URLs for all tiles covering the specified area.
        """
        start_x, start_y = wgs84_to_pixels(west_longitude, north_latitude, zoom)
        end_x, end_y = wgs84_to_pixels(east_longitude, south_latitude, zoom)

        urls = [
            self._provider_url.format(style=style, x=x, y=y, zoom=zoom)
            for y in range(start_y, end_y + 1)
            for x in range(start_x, end_x + 1)
        ]
        return urls

    def _get_map_tiles(
            self,
            north_latitude: float,
            west_longitude: float,
            south_latitude: float,
            east_longitude: float,
            zoom: int,
            map_style: str,
    ) -> Tuple[List[bytes], int]:
        """
        Download map tiles from the provider.

        :param north_latitude: Northern latitude of the map section.
        :param west_longitude: Western longitude of the map section.
        :param south_latitude: Southern latitude of the map section.
        :param east_longitude: Eastern longitude of the map section.
        :param zoom: Zoom level.
        :param map_style: Map style.
        :return: Map tiles as byte objects and the actual zoom level.
        """
        success = False
        map_tiles = None
        while not success and zoom >= GoogleMapsDownloader.MIN_ZOOM:
            download_urls = self._get_urls(
                north_latitude,
                west_longitude,
                south_latitude,
                east_longitude,
                zoom,
                self._styles.get(map_style, self._default_style),
            )
            map_tiles, success = self._url_downloader(download_urls)
            if not success:
                log(
                    level=WARNING,
                    msg=ValueError(
                        f"Unfortunately, this provider does NOT support zoom level {zoom}"
                        f" for the given geographical coordinates and style. Trying zoom level {zoom - 1}."
                    )
                )
                zoom -= 1

        return map_tiles, zoom

    @staticmethod
    def _merge_tiles(
            tiles,
            north_latitude: float,
            west_longitude: float,
            south_latitude: float,
            east_longitude: float,
            zoom: int,
    ) -> Image:
        """
        Merge individual map tiles into a single map image.

        :param tiles: Map tiles as byte objects.
        :param north_latitude: Northern latitude of the map section.
        :param west_longitude: Western longitude of the map section.
        :param south_latitude: Southern latitude of the map section.
        :param east_longitude: Eastern longitude of the map section.
        :param zoom: Zoom level.
        :return: The combined map section as a PIL Image object.
        """
        start_x, start_y = wgs84_to_pixels(west_longitude, north_latitude, zoom)
        end_x, end_y = wgs84_to_pixels(east_longitude, south_latitude, zoom)

        width = end_x - start_x + 1
        height = end_y - start_y + 1
        map_image = Image.new("RGBA", (width * 256, height * 256))

        for tile_index, tile_data in enumerate(tiles):
            tile_image = Image.open(io.BytesIO(tile_data))
            x = tile_index % width
            y = tile_index // width
            map_image.paste(tile_image, (x * 256, y * 256))

        return map_image

    @staticmethod
    def _postprocess_image(
            image: Image,
            image_format: str = "RGB",
            resize: Union[None, Tuple[int, int]] = None,
            return_type: Union[str] = "PIL",
    ) -> Union[Image.Image, np.ndarray, bytes]:
        """
        Postprocess the map image.

        :param image: The map image.
        :param image_format: Image format. Supported formats are "RGB" and "RGBA".
        :param resize: New size of the map section is a tuple (width, height) or (None, height) or (None, width).
        If both are provided, the aspect ratio may be distorted. If only one is provided, the original aspect ratio is
        maintained. If None, the original size is used.
        :param return_type: The type of the returned object. Supported types are "PIL", "numpy", and "bytes".
        :return: The postprocessor map image. It can be a PIL Image object, a NumPy array, or a byte object, depending
        on the return_type parameter.
        """
        if resize:
            image = resize_image(image, resize)

        image = image.convert(image_format)

        if return_type == "PIL":
            return image
        elif return_type == "numpy":
            return np.array(image)
        elif return_type == "bytes":
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            return buffer.getvalue()
        else:
            raise ValueError("Unsupported return type.")

    @property
    def styles(self) -> List[str]:
        """Return the supported map styles."""
        return list(self._styles.keys())

    @property
    def default_style(self) -> str:
        """Return the default map style."""
        return self._default_style
