# read version from installed package
from importlib.metadata import version

__version__ = version("odineye")


from odineye.maps_downloaders.google_maps_downloader import GoogleMapsDownloader
