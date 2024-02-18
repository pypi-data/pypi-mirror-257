from math import floor, pi, log, tan


def wgs84_to_pixels(longitude: float, latitude: float, zoom: int) -> (int, int):
    """
    Convert WGS84 coordinates to tile coordinates.

    :param longitude: Longitude.
    :param latitude: Latitude.
    :param zoom: Zoom level.
    :return: Tile coordinates (x, y).
    """
    if not (isinstance(longitude, (int, float)) and isinstance(latitude, (int, float))):
        raise TypeError("Longitude and latitude must be int or float!")

    longitude_normalized = (longitude + 180) / 360
    latitude_radians = log(tan((90 + latitude) * pi / 360)) / (pi / 180)
    latitude_normalized = 1 - ((latitude_radians + 180) / 360)

    tiles_count = 2 ** zoom
    x = floor(longitude_normalized * tiles_count)
    y = floor(latitude_normalized * tiles_count)

    return x, y
