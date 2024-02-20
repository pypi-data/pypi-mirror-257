from abc import ABC
from typing import Tuple, Union


class MapsDownloader(ABC):
    """An abstract class for downloading map sections from various map providers."""

    MAX_LATITUDE = 85.0511287798
    MAX_LONGITUDE = 180.0

    def validate(
            self,
            north_latitude: float,
            west_longitude: float,
            south_latitude: float,
            east_longitude: float,
            zoom: int,
            style: str,
            image_format: str = "RGB",
            resize: Union[None, Tuple[int, int]] = None,
            return_type: str = Union["PIL", "numpy", "bytes"],
    ):
        """
        Validates all input parameters and calls the internal methods to download and process the map section.

        :param north_latitude: Northern latitude of the map section.
        :param west_longitude: Western longitude of the map section.
        :param south_latitude: Southern latitude of the map section.
        :param east_longitude: Eastern longitude of the map section.
        :param zoom: Zoom level.
        :param style: Map style.
        :param image_format: Image format. Supported formats are "RGB" and "RGBA".
        :param resize: New size of the map section is a tuple (width, height) or (None, height) or (None, width).
        If both are provided, the aspect ratio may be distorted. If only one is provided, the original aspect ratio is
        maintained. If None, the original size is used.
        :param return_type: The type of the returned object. Supported types are "PIL", "numpy", and "bytes".
        :return: The combined map section. It can be a PIL Image object, a NumPy array, or a byte object, depending
        on the return_type parameter.
        """
        self._validate_latitude(north_latitude)
        self._validate_latitude(south_latitude)
        self._validate_longitude(west_longitude)
        self._validate_longitude(east_longitude)

        self._validate_style(style)
        self._validate_resize(resize)
        assert north_latitude > south_latitude, "North latitude must be greater than south latitude."
        assert east_longitude > west_longitude, "East longitude must be greater than west longitude."
        assert isinstance(zoom, int), "Zoom level must be an integer."
        assert image_format in ["RGB", "RGBA"], "Image format must be 'RGB' or 'RGBA'."
        assert return_type in ["PIL", "numpy", "bytes"], "Return type must be 'PIL', 'numpy', or 'bytes'."

    def download(
            self,
            north_latitude: float,
            west_longitude: float,
            south_latitude: float,
            east_longitude: float,
            zoom: int,
            style: str,
            image_format: str = "RGB",
            resize: Union[None, Tuple[int, int]] = None,
            return_type: str = Union["PIL", "numpy", "bytes"],
    ):
        """
        Download a map section given geographical coordinates, zoom level, and style.

        :param north_latitude: Northern latitude of the map section.
        :param west_longitude: Western longitude of the map section.
        :param south_latitude: Southern latitude of the map section.
        :param east_longitude: Eastern longitude of the map section.
        :param zoom: Zoom level.
        :param style: Map style.
        :param image_format: Image format. Supported formats are "RGB" and "RGBA".
        :param resize: New size of the map section is a tuple (width, height) or (None, height) or (None, width).
        If both are provided, the aspect ratio may be distorted. If only one is provided, the original aspect ratio is
        maintained. If None, the original size is used.
        :param return_type: The type of the returned object. Supported types are "PIL", "numpy", and "bytes".
        :return: The combined map section. It can be a PIL Image object, a NumPy array, or a byte object, depending
        on the return_type parameter.
        """
        raise NotImplementedError("The download method must be implemented in a derived class.")

    def _validate_latitude(self, latitude: float):
        assert abs(latitude) <= self.MAX_LATITUDE, \
            f"Latitude must be between -{self.MAX_LATITUDE} and {self.MAX_LATITUDE} degrees."

    def _validate_longitude(self, longitude: float):
        assert abs(longitude) <= self.MAX_LONGITUDE, \
            f"Longitude must be between -{self.MAX_LONGITUDE} and {self.MAX_LONGITUDE} degrees."

    @staticmethod
    def _validate_style(style: str):
        assert isinstance(style, str), "Map style must be a string."
        if style not in ["satellite", "hybrid", "roadmap"]:
            raise ValueError("Map style must be 'satellite', 'hybrid', or 'roadmap'.")

    @staticmethod
    def _validate_resize(resize: Union[None, Tuple[int, int]]):
        if resize is not None:
            assert isinstance(resize, tuple) and len(resize) == 2, "Resize must be a tuple of two integers."
