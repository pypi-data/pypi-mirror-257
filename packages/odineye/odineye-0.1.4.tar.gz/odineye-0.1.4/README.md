<br>
<div align="center">
    <a href="https://github.com/NaturalStupidlty/odineye/blob/main/.github/workflows/ci-cd.yml"><img src="https://github.com/NaturalStupidlty/odineye/actions/workflows/ci-cd.yml/badge.svg" alt="OdinEye CI"></a>
    <a href="https://codecov.io/gh/NaturalStupidlty/odineye"><img src="https://codecov.io/gh/NaturalStupidlty/odineye/developmnet/graph/badge.svg?token=YGOUAPRFX8" alt="OdinEye Code Coverage"></a>

</div>
<br>

## <div align="center">📕 <a href="https://odineye.readthedocs.io/en/latest/">Documentation</a> </div>

See below for a quickstart installation and usage example, and see the 
[OdinEye Docs](https://odineye.readthedocs.io/en/latest/) for full documentation.

<details open>
<summary>Installation</summary>

Pip install the odineye package including all 
[requirements](https://github.com/NaturalStupidlty/odineye/blob/main/pyproject.toml) in a 
[**Python>=3.8**](https://www.python.org/) environment.

[![PyPI version](https://badge.fury.io/py/odineye.svg)](https://badge.fury.io/py/odineye) [![Downloads](https://static.pepy.tech/badge/odineye)](https://pepy.tech/project/odineye)

```bash
pip install odineye
```

</details>

<details open>
<summary>Usage</summary>

## <div align="center"> 🐍 Python</div>

**OdinEye** can be used to download satellite maps given _**latitude**_ and _**longitude**_. 
Here is an example with the location of Vancouver Public Library in Canada:

```python
from odineye import GoogleMapsDownloader

north_latitude, west_longitude = (49.280446, -123.116502)
south_latitude, east_longitude = (49.279118, -123.114704)

downloader = GoogleMapsDownloader()
map_picture = downloader.download(
    north_latitude,
    west_longitude,
    south_latitude,
    east_longitude,
    zoom=20,
    map_style="satellite",
)
map_picture.save("assets/pictures/demo_map.png")
```

The resulting map looks like this:

<div style="text-align:center">
    <img src="https://raw.githubusercontent.com/NaturalStupidlty/odineye/main/assets/pictures/demo_map.png" alt="Map" width="400"/>
</div>

</details>

<br>

## <div align="center"> 🤓 License</div>

OdinEye was created by **[NaturalStupidlty](https://github.com/NaturalStupidlty)**.

It is licensed under the terms of the GNU General Public License v3.0 license.
