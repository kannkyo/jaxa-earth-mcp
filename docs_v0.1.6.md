<!-- START OF FILE: api-reference-detail.en.md -->
# API Reference: jaxa.earth.je


    This API package for Python has developed to utillize various Earth 
    observation data held by [JAXA](https://www.jaxa.jp/). By using this API, you can easily acquire and 
    process data without worrying about the specifications, sensors, resolution, 
    etc. of each satellite data.

    je module contains four classes : ``FeatureCollection``, ``ImageCollectionList``,
    ``ImageCollection``, ``ImageProcess``.

    Example:
        ```python
        # Usage example        
    
        # Import module
        from jaxa.earth import je
        
        # Read geojson
        geoj_path = "gadm36_JPN_0.geojson"
        geoj = je.FeatureCollection().read(geoj_path).select([])
        
        # Get images
        data_out = je.ImageCollection("JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global")\
                     .filter_date(["2021-01-01T00:00:00","2022-01-01T00:00:00"])\
                     .filter_resolution(20)\
                     .filter_bounds(geoj[0])\
                     .select("DSM")\
                     .get_images()
        
        # Process and show images
        img = je.ImageProcess(data_out)\
                .show_images()\
                .calc_spatial_stats()\
                .show_spatial_stats()
        ```


## Class: `FeatureCollection`


    The ``FeatureCollection`` class is used to read a feature collection and select 
    features of geojson data from your computer.

    Returns:
        A ``FeatureCollection`` class object which has a properry of ``feature_collection``.
        the object's properties are set to None by default.

    Attributes:
        feature_collection (dict): The property is updated after the method ``read`` 
            is executed. The default value is None.

    Example:
        ```python
        # Usage example: Aquire feature collection data
        geoj_path = "C:\MyData\gadm36_JPN_1.geojson"
        geoj = je.FeatureCollection().read(geoj_path).select(["Tokyo"])
        ```
    

### Method: `__init__(self)`

### Method: `read(self, path: str)`


        The method ``read`` reads the inputed path's geojson data as feature collection.
        
        Args:
            path (str): The absolute path to the user's geojson location.

        Returns:
            A ``FeatureCollection`` class object which stores updated ``feature_collection`` property

        Example:
            ```python
            # Usage example: Read geojson data as feature collection
            data_path = "C:\MyData\MyArea.geojson"
            data_fc   = je.FeatureCollection.read(data_path)
            ```
        

### Method: `select(self, keywords: list = [])`


        The method ``select`` filter the inputed feature collection's data in 
        properties by keywords. The default is blank list, so all features of 
        feature collection are selected.

        Args:
            keywords (list): keywords list of your preferred words.

        Returns:
            list : geojson features selected by keywords

        Example:
            ```python
            # Usage example: Select feature from geojson's feature collection
            geojson = data_fc.select(["Japan","Tokyo"])
            ```
        

## Class: `ImageCollection`


    The class, ``ImageCollection`` gets selected collection's catalog json data from
    JAXA Earth database. When you use the class's method, you can acquire collection's
    raster images depending on query such as date limit, resolution, bounds and band. 

    Args:
        collection (str): Name of the selected collection. If not specified, 
            "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global" is used.
        stac_cog_url (str): Users can set valid stac cog url to ``stac_cog_url``.
        ssl_verify (bool): Users can set valid ssl certification process to ``True``
            or ``False``. The default is ``True``. Note: Setting the value to ``False`` can be a security risk.

    Returns:
        An ``ImageCollection`` class object which has properties of ``stac_date``,
        ``stac_ppu`` , ``stac_bounds`` , ``stac_band`` and ``raster``. 
        All properties of the object are set to Noe by default.

    Attributes:
        stac_date (A ``Stac`` class object): The default value is None. The updated property 
            is set after the method, ``filter_date``. The updated property has four 
            properties such as ``query`` , ``url`` , ``id`` and ``json``. The object is 
            used as input to the method ``filter_resolution``. 
        stac_ppu (A ``Stac`` class object): The default value is None. The updated property 
            is set after the method, ``filter_resolution``. The updated property has 
            three properties such as ``query`` , ``url`` and ``json``. The object is 
            used as input to the method ``filter_bounds``. 
        stac_bounds (A ``Stac`` class object): The default value is None. The updated property 
            is set after the method, ``filter_bounds``. The updated property has three 
            properties such as ``query`` , ``url`` and ``json``. The object 
            is used as input to the method ``select``. 
        stac_band (A ``Stac`` class object): The default value is None. The updated property 
            is set after the method, ``select``. The updated property has two properties such 
            as ``query`` and ``url``. The object is used as input to the method ``get_images``. 
        raster (A ``Raster`` class object): The default value is None. The updated property 
            is set after the method, ``get_images``. The updated ``Raster`` class 
            object property has properties of ``img`` , ``latlim`` and ``lonlim``. 

    Example:
        ```python
        # Usage example: Get image
        data_out = je.ImageCollection("JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global")\
                     .filter_date(["2021-01-01T00:00:00","2023-01-31T00:00:00"])\
                     .filter_resolution(20)\
                     .filter_bounds([-180,-90,180,90])\
                     .select("DSM")\
                     .get_images()
        ```
    

### Method: `__init__(self, collection: str = None, stac_cog_url: str = None, ssl_verify: bool = None)`

### Method: `filter_bounds(self, bbox: list = None, geoj: dict = None)`


        The method, ``filter_bounds`` filters collection's catalog json 
        by the user query of bounds or geojson. If you input both of bbox and geoj,
        geoj is used to detect bounding box. If you don't input neither of them,
        maximum bounding box is selected. 
        In QGIS environment, appropriate area is selected with no input. 
        The property of ``stac_bounds`` is updated after the method.

        Args:
            bbox (list): bounding box input.
            geoj (dict): geojson input

        Returns:
            An ``ImageCollection`` class object that stores updated ``stac_bounds`` property

        Note:
            Attention! You have to use method ``filter_resolution`` before the method.

        Example:
            ```python
            # Usage example: Filter ImageCollection by bbox of geojson
            bbox = [120,20,150,50]
            data_ic3 = data_ic2.filter_bounds(bbox)
            ```
        

### Method: `filter_date(self, dlim: list = [])`


        The method, ``filter_date`` filters collection's catalog json by the user query of
        date limit. If no input is given, default date lim parameter is set as 
        ["2021-01-01T00:00:00","2021-12-31T23:59:59"]. The property of ``stac_date``  
        is updated after the method.

        Args:
            date_lim (list): date limits of minimum date, maximum date.

        Returns:
            An ``ImageCollection`` class object that stores updated ``stac_date`` property

        Note:
            If normal products are specified for multiple years, the same products is returned for multiple years .

        Example:
            ```python
            # Usage example: Filter ImageCollection by date limit
            date_lim = ["2021-01-01T00:00:00","2022-01-01T00:00:00"]
            data_ic1 = data_ic0.filter_date(date_lim)
            ```
        

### Method: `filter_resolution(self, ppu: float = None)`


        The method, ``filter_resolution`` filters collection's catalog json 
        by the user query of resolution of ppu (Pixels Per Unit). Unit means one 
        degree in epsg 4326, 32786m in epsg 3995. If no input is given, minimum value or
        appropriate value (in QGIS only) is set. The property of ``stac_ppu`` 
        is updated after the method.

        Args:
            ppu (float): ppu input.

        Returns:
            An ``ImageCollection`` class object that stores updated ``stac_ppu`` property

        Note:
            Attention! You have to use method ``filter_date`` before the method.

        Example:
            ```python
            # Usage example: Filter ImageCollection by ppu
            ppu = 20
            data_ic2 = data_ic1.filter_resolution(ppu)
            ```
        

### Method: `get_images(self)`


        The method, ``get_images`` gets collection's images depending on the user's 
        queries of date limit, resolution, bounds and band. The property of ``raster`` will 
        be updated after the method. In addition to this, region of interest area of
        ``raster`` images will be returned.

        Returns:
            An ``ImageCollection`` class object that stores updated ``raster`` property

        Note:
            Attention! You have to use method ``filter_band`` before the method.

        Example:
            ```python
            # Usage example: Get Image depend on user's query.
            data_out0 = data_ic4.get_images()
            ```
        

### Method: `select(self, band: str = None)`


        The method, ``select`` selects collection's catalog json 
        by the user query of band. If you don't input band, the first
        band is selected. Property of ``stac_band`` will 
        be updated after the method.

        Args:
            band (str): band of asset

        Returns:
            An ``ImageCollection`` class object that stores updated ``stac_band`` property

        Note:
            Attention! You have to use method ``filter_bounds`` before the method.

        Example:
            ```python
            # Usage example: Filter ImageCollection by band
            band = "DSM"
            data_ic4 = data_ic3.filter_band(band)
            ```
        

## Class: `ImageCollectionList`


    The class, ``ImageCollectionList`` gets and filters collection's catalog json 
    depending on user input keywords.

    Args:
        ssl_verify (bool): Users can set valid ssl certification process to ``True``
            or ``False``. The default is ``True``. Note: Setting the value to ``False`` can be a security risk.

    Returns:
        An ``ImageCollectionList`` class object which has properties of ``stac_collections``.

    Example:
        ```python
        # Usage example: Get collection's name and band
        keywords = ["LST","_half-month"]
        collections,bands = je.ImageCollectionList(ssl_verify=False)\
                              .filter_name(keywords=keywords)
        ```
    

### Method: `__init__(self, ssl_verify: bool = None)`

### Method: `filter_name(self, keywords: list = [])`


        The method, ``filter_name`` filter collection's catalog json from 
        collection's id depending on user input keywords. 
        
        Args:
            keywords (list): keywords of request.

        Returns:
            filtered collections and filtered bands

        Example:
            ```python
            # Usage example: Get collection's name and band
            key = ["LST","_half-month"]
            collections,bands = je.ImageCollectionList()\
                                  .filter_name(keywords=key)
            ```
        

## Class: `ImageProcess`


    The class, ``ImageProcess`` execute various process by using inputed ``ImageCollecion``
    class objects. When you use ``ImageProcess`` class method, you can process and get
    images such as masking images, differential images and calculated temporal/spatial 
    statistics. In addition to the processing, it's possible to show images or 
    timeseries graph. 

    Args:
        data (object): ``ImageCollection`` class object which contains 
            updated ``raster`` property.
            Note: The ``ImageCollection`` object must have correct ``raster`` property.

    Returns:
        An ``ImageProcess`` class object with updated property

    Attributes:
        raster (A ``Raster`` class object): The default value is same as inputed 
            ``ImageCollection`` class object's  ``raster`` property. The property
            is updated after  executing methods of the ``ImageProcess``  class object, 
            such as ``mask_images`` , ``diff_images`` and ``calc_temporal_stats``.
        timeseries (dict): The default value is None. The property is updated after  
            executing methods of the ``ImageProcess`` class object, such as ``calc_spatial_stats``.
            The updated property has five keys and values such as "mean", "std", "min", "max" and  
            "median".

    Example:
        ```python
        # Usage example: Process and show images
        img = je.ImageProcess(data_out0)\
                .show_images()\
                .calc_spatial_stats()\
                .show_spatial_stats()
        ```
    

### Method: `__init__(self, data)`

### Method: `calc_spatial_stats(self)`


        The method, ``calc_spatial_stats`` calculate spatial statistics.

        Returns:
            An ``ImageProcess`` class object that stores updated ``timeseries`` property.
            The updated property has five keys and values such as "mean", "std", "min", "max" and 
            "median".

        Example:
            ```python
            # Usage example: Calculate spatial stats of data_ip0
            data_s_stats = data_ip0.calc_spatial_stats()
            ```
        

### Method: `calc_temporal_stats(self, method_query: str = 'mean')`


        The method, ``calc_temporal_stats`` calculate temporal statistics by user 
        inputed query of method_query.

        Args:
            method_query (dict): "mean" or "max" or "min" or "std" or "median".
                The default is "mean".

        Returns:
            An ``ImageProcess`` class object that stores the updated ``raster`` property

        Example:
            ```python
            # Usage example: Calculate temporal stats of data_ip0
            data_t_stats = data_ip0.calc_temporal_stats("mean")
            ```
        

### Method: `diff_images(self, ref)`


        The method, ``diff_images`` take difference by user inputed query of ref.

        Args:
            ref (object): ``ImageCollection`` class object that has updated ``raster`` 
                property which is used as ref data.
                Note: The shape of the ref (including resolution) must be the same as the data.

        Returns:
            An ``ImageProcess`` class object that stores the updated ``raster`` property

        Example:
            ```python
            # Usage example: Differential data(data_out0-data_out1)
            data_diff = data_ip0.diff_images(data_out1)
            ```
        

### Method: `mask_images(self, mask, method_query: str = 'values_equal', values: float = [0, 1])`


        The method, ``mask_images`` masks by using mask, type_query and values.

        Args:
            mask (class): ``ImageCollection`` class object that has updated ``raster`` 
                property which is used as masking data.
                Note: The shape of the mask (including resolution) must be the same as the data.

            method_query (dict): "range" or "values_equal" or "bits_equal". 
                The default method is "values_equal".
                
                "range" is used when users would like to extract a specific range of 
                values and mask values outside the range. The data type of float is acceptable 
                as a "range" mask.

                "values_equal" is used when users would like to extract only certain bit 
                values of pixels and mask other bit values of pixels. The data type of float is 
                acceptable. Typically, land cover products is used as "values_equal" 
                mask.

                "bits_equal" is used when users would like to extract only certain values 
                of pixels and mask other bit values of pixels. The data type of float is 
                not acceptable as a mask. Typically, quality assurance products is 
                used as a "bits_equal" mask.

            values(list): user query of values list. if you set type_query as "range",
                please set two values, minimum and maximum. If "values_equal",
                you can set multiple values list as you like. If "bits_equal", you can set
                bit values 0 or 1 as bit values which begins from zero bit.
                The default value is [0,1].

        Returns:
            An ``ImageProcess`` class object that stores the updated ``raster`` property

        Example:
            ```python
            # Usage example: Mask data_out0 by data_out1
            data_masked = data_ip0.mask_images(data_out1,"range",[0,100])
            ```
        

### Method: `show_images(self, cmap: str = None, clim: list = [], output: str = 'show')`


        The method, ``show_images`` shows images of ``raster`` property. If multiple
        date's image is set, the method shows all of the images.

        Args:
            cmap (str): query of colormap name. User can choose "ndvi","turbo" and 
                "spectral". The default is "turbo".

            clim (list): query of color range (optional).
            output (str): query of output method. User can choose "show" or "png_buffer".

        Returns:
            An ``ImageProcess`` class object

        Example:
            ```python
            # Usage example: Show images of data_ip0
            data_ip0.show_images()
            ```
        

### Method: `show_images_qgis(self, cmap: str = None, clim: list = [])`


        The method, ``show_images_qgis`` shows images in qgis.

        Args:
            cmap (str): query of colormap name. User can choose "ndvi","turbo" and 
                "spectral". Default is "turbo".
            clim (list): query of color range (optional).

        Returns:
            An ``ImageProcess`` class object

        Note:
            Attention! This method is only valid in QGIS environment.

        Example:
            ```python
            # Usage example: Show images of data_ip0 in qgis
            data_ip0.show_images_qgis()
            ```
        

### Method: `show_spatial_stats(self, ylim: list = [], output: str = 'show')`


        The method, ``show_spatial_stats`` shows graph of calculation result of 
        the method ``calc_spatial_stats``.

        Args:
            ylim (list): query of color range (optional)
            output (str): query of output method. User can choose "show" or "png_buffer".

        Returns:
            An ``ImageProcess`` class object

        Note:
            Attention! You should use the method ``calc_spatial_stats`` before the method.

        Example:
            ```python
            # Usage example: Show graph of calclation result of the method calc_spatial_stats
            data_s_stats.show_spatial_stats()
            ```
        


---

<!-- START OF FILE: api-reference.en.md -->
# API Reference

`jaxa.earth.je` module contains four classes:
`FeatureCollection`, `ImageCollectionList`, `ImageCollection`, `ImageProcess`.

```python
from jaxa.earth import je
```

---

::: jaxa.earth.je
    options:
      members:
        - FeatureCollection
        - ImageCollectionList
        - ImageCollection
        - ImageProcess
      show_root_heading: false
      show_root_toc_entry: false
      heading_level: 2
      show_source: false
      members_order: source


---

<!-- START OF FILE: documents.en.md -->
# Documents

## How to Use the API for Python with QGIS (Japanese)

A document on how to use the JAXA Earth API for Python with QGIS is available in Japanese as a PDF file.

Please make use of this document for your research using the API or for studying application cases.

[:material-file-pdf-box: How_to_Use_the_API_for_Python_with_QGIS_jp.pdf](assets/files/How_to_Use_the_API_for_Python_with_QGIS_jp.pdf)



---

<!-- START OF FILE: getting-started.en.md -->
# Getting Started

## Install Python

If you don't have a Python environment, install Python from the official site.
The API was generated and checked in Python 3.8.10 and above.

<https://www.python.org/>

## Install QGIS (optional)

If you would like to use the API in QGIS, install QGIS from the official site.
The API was checked in QGIS 3.10.6.

<https://qgis.org/>

## How to use JAXA Earth API for Python

### With install

**Case 1: Install via PyPI (recommended)**

```bash
pip install jaxa-earth
```

**Case 2: Download and install**

Download the package and install:

[:material-download: jaxa-earth-0.1.6.zip](assets/files/jaxa-earth-0.1.6.zip)

```bash
pip install jaxa-earth-0.1.6.zip
```

Module packages and dependent packages the API depends on are also installed:

- `matplotlib`
- `requests`

### Verify installation

Launch Python and check the API is installed correctly:

```python
from jaxa.earth import je
```

If no error occurs, you have installed the API module correctly.

### Without install

Unzip the package and add the path to your Python scripts:

```python
import sys
sys.path.append("C://YOUR-FOLDER-PATH/jaxa-earth-0.1.6")
from jaxa.earth import je
```

## Minimal usage example

```python
from jaxa.earth import je

# Get an image using all default parameters
data = je.ImageCollection(ssl_verify=True) \
         .filter_date() \
         .filter_resolution() \
         .filter_bounds() \
         .select() \
         .get_images()

# Show the image
img = je.ImageProcess(data) \
        .show_images()
```

!!! note
    If you encounter an SSL error, set `ssl_verify=False`.


---

<!-- START OF FILE: index.en.md -->
# JAXA Earth API for Python

[![PyPI version](https://img.shields.io/badge/PyPI-v0.1.6-blue?logo=pypi&logoColor=white)](https://pypi.org/project/jaxa-earth/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-lightgrey)](https://data.earth.jaxa.jp/license/)

<div style="text-align:center">
<iframe width="560" height="315" src="https://www.youtube.com/embed/FnD86JcFxoc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## Overview

[JAXA Earth API](https://data.earth.jaxa.jp/) has been developed to utilize various Earth
observation data held by [JAXA](https://www.jaxa.jp/).
This API package for Python is designed to easily acquire and
process data without worrying about the specifications, sensors, resolution,
etc. of each satellite data.

## Quick Example

```python
from jaxa.earth import je

# Read geojson
geoj = je.FeatureCollection().read("gadm36_JPN_0.geojson").select([])

# Get images
data_out = je.ImageCollection("JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global") \
             .filter_date(["2021-01-01T00:00:00","2022-01-01T00:00:00"]) \
             .filter_resolution(20) \
             .filter_bounds(geoj[0]) \
             .select("DSM") \
             .get_images()

# Process and show images
img = je.ImageProcess(data_out) \
        .show_images() \
        .calc_spatial_stats() \
        .show_spatial_stats()
```

## PyPI Repository

<https://pypi.org/project/jaxa-earth/>

## API document for AI
<https://data.earth.jaxa.jp/api/python/v0.1.6/docs.md>

## License

<https://data.earth.jaxa.jp/license/>



---

<!-- START OF FILE: release-notes.en.md -->
# Release Notes

!!! tip "Latest version"
    **v0.1.6** — `pip install jaxa-earth`

## Version 0.1.6

Compatible with COG/STAC database version v1.2.

Reference: <https://data.earth.jaxa.jp/api/python/v0.1.6/>

### API

- Added a function to read hourly products.

### Documentation

- Changed the official repository from JAXA to pypi.org.
- Added documentation for installing via `pip`.

---

## Version 0.1.5

Compatible with COG/STAC database version v1.2.

Reference: <https://data.earth.jaxa.jp/api/python/v0.1.5/>

### API

- Added a function to output `png_buffer` in displaying images for MCP function.

### Documentation

- Added documentation for using local MCP Server in Claude Desktop.

---

## Version 0.1.4

Compatible with COG/STAC database version v1.2.

Reference: <https://data.earth.jaxa.jp/api/python/v0.1.4/>

### API

- Added a function to process 8-day normal data.

### Documentation

- Added documentation for using Google Colab.

---

## Version 0.1.3

Compatible with COG/STAC database version v1.2.

Reference: <https://data.earth.jaxa.jp/api/python/v0.1.3/>

### API

- Small bug fixed.

---

## Version 0.1.2

Compatible with COG/STAC database version v1.2.

Reference: <https://data.earth.jaxa.jp/api/python/v0.1.2/>

### API

- Changed the specification so that nodata becomes transparent when label data such as RGB, LCCS, and FNF are displayed in QGIS.

### COG

- Changed the COG placement position to the same position as STAC and made it a relative path.
- Support for 16-bit color map input for label data such as RGB, LCCS, and FNF.
- Added map projection specification for Antarctica (EPSG3031).
- Changed the allowable range of longitude from ±180 deg to ±360 deg in EPSG4326.
- Added `GEO_METADATA` tag available in Web Map Service API.
- Added `GDAL_NODATA` tag.


---

<!-- START OF FILE: mcp-server.en.md -->
# Using the API as MCP Server Tools in Claude Desktop

This page explains how to install the `jaxa-earth` package in a local Python virtual environment, configure Claude Desktop to use a local MCP server, and verify the integration on your PC.

![MCP Server overview](assets/images/mcpserver/figure_mcp01.png)

## Set Up a Virtual Environment

Open PowerShell (recommended) or Command Prompt. From a working folder, create a venv:

```powershell
python -m venv venv
```

Activate the venv:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the API:

```powershell
# From PyPI
pip install jaxa-earth

# Or from a downloaded zip
pip install ./jaxa-earth-0.1.6.zip
```

Install the additional MCP dependency:

```powershell
pip install mcp
```

## Prepare the MCP Server Script

Download `mcp_server.py` and copy it into a stable path inside or reachable from your environment.

[:material-download: mcp_server.py](assets/files/mcp_server.py)

Common placement choices:

- The working folder alongside the venv
- `C:\YOUR-WORKING-FOLDER-PATH\mcp_server.py`

Make sure the Python interpreter referenced in the configuration points to the venv Python executable:

```
C:\YOUR-WORKING-FOLDER-PATH\venv\Scripts\python.exe
```

## Configure Claude Desktop

Open Claude Desktop and go to:

**Settings → Desktop app → Local MCP servers → Edit config**

Add the following configuration:

```json
{
    "mcpServers": {
        "jaxa_api_tools": {
            "command": "C:\\YOUR-WORKING-FOLDER-PATH\\venv\\Scripts\\python",
            "args": ["C:\\YOUR-WORKING-FOLDER-PATH\\mcp_server.py"]
        }
    }
}
```

- `command` must be the **full path** to the Python executable inside the venv.
- `args` must include the **full path** to `mcp_server.py`.

## Restart Claude Desktop

Completely exit Claude Desktop.

!!! warning
    Even after closing the application window, Claude Desktop may still be running in the background. Make sure it is fully stopped before restarting.

After restarting, verify that the tool is enabled in the MCP tools panel.

![Verify tool enabled](assets/images/mcpserver/figure_mcp02.png)

## Available Tools

Once enabled, the following four JAXA Earth API tools are available in Claude Desktop:

| Tool | Description |
|------|-------------|
| `search_collections_id` | Return JAXA Earth API's detailed collection information. |
| `show_images` | Show satellite image using JAXA Earth API based on user input. |
| `calc_spatial_stats` | Calculate satellite data's spatial statistics values based on user input. |
| `show_spatial_stats` | Show satellite data's spatial statistics result image based on user input. |

## Sample Questions

![Sample question 1](assets/images/mcpserver/figure_mcp03.png)

![Sample question 2](assets/images/mcpserver/figure_mcp04.png)


---

<!-- START OF FILE: access-analysis.en.md -->
# Access Analysis Tool with Metabase

## Overview

In the JAXA Earth Database for API, COG/STAC data are stored in cloud storage (currently Wasabi).
When a user accesses the database, a text-based access log is generated.

This tool is a dashboard viewing tool to analyze user access to COG data and investigate usage trends.

**Components:**

| Component   | Role                              |
|-------------|-----------------------------------|
| Docker      | Virtual environment               |
| Python      | Log analysis                      |
| PostgreSQL  | Database                          |
| Metabase    | BI (Business Intelligence) tool   |

## How to Use the Access Analysis Tool

### Configure environment and convert logs to PostgreSQL database

1. **Install Docker** in your environment.
2. **Download and unzip** the tool.

    [:material-download: Access_Analysis_Tool.zip](assets/files/Access_Analysis_Tool.zip)

3. Create a folder to save logs. By default, `C:/wasabi_log` is configured as a volume in `docker-compose.yml` — adjust as needed.
4. Change your current directory to the location of the `Dockerfile`.
5. Run:

```bash
docker-compose up -d --build
```

6. **Activate the Python remote container** using a development environment such as VS Code Remote Explorer.
7. Set your ID and Secret in `set_secret.py`.
8. Execute `main.py` inside the container to fetch logs.

Once complete, Wasabi logs are registered in PostgreSQL.

!!! warning
    Logs obtained from Wasabi are **deleted from the cloud** and stored locally. Handle raw logs with care.

### Metabase configuration and dashboard creation

1. Access the following address with a browser to start Metabase:

    ```
    localhost:443
    ```

2. Enter your country, email, name, etc.
3. Select **PostgreSQL** as the database and enter:

    | Field           | Value      |
    |-----------------|------------|
    | Host            | `db`       |
    | Port            | `5432`     |
    | Database name   | `postgres` |
    | Username        | `postgres` |
    | Password        | `metabase` |

4. You can now access PostgreSQL from Metabase.

To update the database, use **Administration → Database → Synchronize with database schema now** and **Rescan field values now**.

The main data is stored in the `Je Pds 20XX` tables.

![Database table list](assets/images/table_list.png)

## Dashboard Examples

### All-collections dashboard

An example dashboard showing download volume rankings and time-series data for each COG collection.

![All-collections dashboard](assets/images/dashboard_all.png)

### Single-collection dashboard

A focused dashboard that visualizes which areas of data are in high demand, organized by COG level.

![Single-collection dashboard](assets/images/dashboard_aw3d.png)

For general Metabase usage, refer to the [official Metabase documentation](https://www.metabase.com/docs/latest/).


---

<!-- START OF FILE: cog-stac-generator.en.md -->
# COG/STAC Generator with Docker

## Overview

This is a generator that takes GeoTIFF data and a configuration JSON file as input and generates COG and STAC files compatible with the JAXA Earth Database for API.

## How to Use the Generator

1. **Install Docker** in your environment.
2. **Download and unzip** the generator package.

    [:material-download: COG_STAC_generator.zip](assets/files/COG_STAC_generator.zip)

3. Change your current directory to the location of the `Dockerfile`.
4. Run:

```bash
docker-compose up -d --build
```

You can then execute `main.py` inside the Docker container to generate COG/STAC.

## Description of Input Parameters

### Parameters in `main.py`

| Parameter      | Description                                      |
|----------------|--------------------------------------------------|
| `root_local`   | Location of COG/STAC output on your environment |
| `bucket`       | Bucket name to be used                           |
| `ftype`        | Fixed with `"cog"`                               |
| `version_path` | Fixed with `"v1"`                                |
| `version_full` | STAC version in JAXA Earth API                   |

### Preparation of GeoTIFFs

Prepared GeoTIFFs must be placed under a date folder. The generator detects dates by folder name:

```
sample_geotiff/
├── 2020-01-01/
│   ├── sample_LST.tif
│   └── sample_LST_QA_flag.tif
└── 2020-01-09/
    ├── sample_LST.tif
    └── sample_LST_QA_flag.tif
```

**Supported date folder types:**

| Date type  | Example              | Description                         |
|------------|----------------------|-------------------------------------|
| YYYY-MM-DD | 2022-01-01           | Daily, 8-day, half-monthly data     |
| YYYY-MM    | 2022-01              | Monthly data                        |
| YYYY       | 2022                 | Yearly data                         |
| DDD        | 001, 365             | Daily normal data                   |
| MM-DD      | 01-01, 12-31         | Half-monthly normal data            |
| MM         | 01, 12               | Monthly normal data                 |

### Configuration Parameters in JSON

The JSON configuration file controls how GeoTIFF files are located and how the STAC file is generated.

**Top-level parameters:**

| Name              | Description                                  |
|-------------------|----------------------------------------------|
| `id`              | Product ID                                   |
| `description`     | Description of the product                   |
| `title`           | Title of the product                         |
| `keywords`        | Keywords: platform, sensor, provider, etc.   |
| `providers`       | Providers information list (`name`, `roles`, `url`) |
| `license`         | Fixed with `"proprietary"`                   |
| `extent`          | Spatial and temporal extent                  |
| `duration`        | Duration: `1D`, `8D`, `HM`, `1M`, `1Y`      |
| `sci:publications`| Publication list                             |

**`summaries` parameters:**

| Name                   | Description                                           |
|------------------------|-------------------------------------------------------|
| `platform`             | Platform of product                                   |
| `instrument`           | Instrument/Sensor of product                          |
| `je:epsg`              | EPSG: `4326` (EQR), `3995` (North pole), `3031` (South pole) |
| `je:stac_date_format`  | Date format: `YYYY-MM/DD`, `YYYY-MM`, `YYYY`, `DDD`, `MM-DD`, `MM` |
| `je:cog_level_max`     | Maximum COG level of product                          |
| `je:ppu_max`           | Maximum PPU (Pixels Per Unit) of product              |
| `je:stac_version`      | STAC version of product                               |

**`assets` / product parameters:**

| Name                      | Description                                                     |
|---------------------------|-----------------------------------------------------------------|
| `title`                   | Title of product                                                |
| `roles`                   | `data`, `data-mask`, or `visual`                                |
| `classification:classes`  | Class data of product                                           |
| `source.path.dir`         | GeoTIFF source directory                                        |
| `source.path.wildcard`    | Wildcard for searching GeoTIFF files                            |
| `source.path.layer_number`| Layer number in GeoTIFF files                                   |
| `source.dn.data_type`     | Data type: `uint8`, `int8`, `uint16`, `int16`, `float32`        |
| `source.dn.nodata`        | Nodata value                                                    |
| `source.dn.error`         | Error values                                                    |
| `source.dn2value`         | Conversion parameters: `slope`, `offset`                        |
| `cog.value.def_interp`    | Interpolation method: `bilinear` or `nearest`                   |
| `cog.value.unit`          | Unit of product                                                 |
| `cog.dn.data_type`        | Output COG data type                                            |
| `cog.dn.min` / `.max`     | Min/Max value in output COG                                     |
| `cog.dn.nodata`           | Nodata value in output COG                                      |
| `cog.dn2value`            | COG output conversion parameters: `slope`, `offset`             |


---

<!-- START OF FILE: database.en.md -->
# Database

## Overview

The database for API contains COG (Cloud Optimized GeoTIFF) and STAC (Spatio Temporal Asset Catalog).

- **COG** is a TIFF format that can be fetched via HTTP range requests depending on the user's area of interest and resolution.
- **STAC** is catalog information in hierarchical JSON format to access COG.

All COG/STAC datasets are visualized and cataloged at:

<https://data.earth.jaxa.jp/en/datasets/>

## COG (Cloud Optimized GeoTIFF)

For general COG information: <https://www.cogeo.org/>

The database defines COG levels so that it can store many kinds of resolution and area levels.
Each COG has up to two internal IMG levels.

![COG structure](assets/images/cog_structure.png)

### COG levels (EPSG4326)

| COG level | Image Size (degree) | IMG level | Image Size (pixels) | PPU   |
|-----------|---------------------|-----------|---------------------|-------|
| level 0   | 180/180 deg         | level 2   | 225/225 pixels      | 1.25  |
|           |                     | level 1   | 450/450 pixels      | 2.5   |
|           |                     | level 0   | 900/900 pixels      | 5     |
| level 1   | 90/90 deg           | level 2   | 900/900 pixels      | 10    |
|           |                     | level 1   | 1800/1800 pixels    | 20    |
|           |                     | level 0   | 3600/3600 pixels    | 40    |
| level 2   | 10/10 deg           | level 2   | 900/900 pixels      | 90    |
|           |                     | level 1   | 1800/1800 pixels    | 180   |
|           |                     | level 0   | 3600/3600 pixels    | 360   |
| level 3   | 1/1 deg             | level 2   | 900/900 pixels      | 900   |
|           |                     | level 1   | 1800/1800 pixels    | 1800  |
|           |                     | level 0   | 3600/3600 pixels    | 3600  |
| level 4   | 0.1/0.1 deg         | level 2   | 900/900 pixels      | 9000  |
|           |                     | level 1   | 1800/1800 pixels    | 18000 |
|           |                     | level 0   | 3600/3600 pixels    | 36000 |

### COG levels (EPSG3995/EPSG3031)

| COG level | Image Size (m)   | IMG level | Image Size (pixels) | PPU |
|-----------|------------------|-----------|---------------------|-----|
| level 0   | 2^24/2^24 m      | level 2   | 512/512 pixels      | 1   |
|           |                  | level 1   | 1024/1024 pixels    | 2   |
|           |                  | level 0   | 2048/2048 pixels    | 4   |
| level 1   | 2^21/2^21 m      | level 2   | 512/512 pixels      | 8   |
|           |                  | level 1   | 1024/1024 pixels    | 16  |
|           |                  | level 0   | 2048/2048 pixels    | 32  |
| level 2   | 2^18/2^18 m      | level 2   | 512/512 pixels      | 64  |
|           |                  | level 1   | 1024/1024 pixels    | 128 |
|           |                  | level 0   | 2048/2048 pixels    | 256 |

## STAC (Spatio Temporal Asset Catalog)

STAC is a hierarchical JSON catalog used to access COG data efficiently.

The STAC COG URL used by this API:

```
https://data.earth.jaxa.jp/stac/cog/v1/catalog.json
```

## PPU (Pixels Per Unit)

PPU (Pixels Per Unit) represents resolution:

- In **EPSG4326**: pixels per 1 degree
- In **EPSG3995/EPSG3031**: pixels per 32786 m

The collection's maximum PPU is selected from the table based on the original data PPU.
For example, if the original data's PPU is 7, the database maximum PPU is 10, and images at 5, 2.5, 1.25 PPU are also generated.


---

<!-- START OF FILE: google-colab.en.md -->
# Getting Data with Google Colab

[Google Colab](https://colab.research.google.com/) is an online platform where you can run Python code and check results without any local setup.

![Google Colab overview](assets/images/googlecolab/image-14.png)

## Set Up Google Colab Environment

### Upload data to Google Drive

Google Colab requires a Google account and Google Drive for data access.

1. Download the sample data and extract it — it contains a `je-sample` directory.

    [:material-download: je-sample.zip](assets/files/je-sample.zip)

2. In Google Drive, create a work folder and drag-and-drop the `je-sample` folder into it.

![Upload to Google Drive](assets/images/googlecolab/image-15.png)

### Load the notebook

1. Go to [Google Colab](https://colab.research.google.com/).
2. Import the `je.ipynb` file from your Google Drive — the code set will be displayed.

![Load notebook](assets/images/googlecolab/image-16.png)

### Mount Google Drive

Run the **Mount Google Drive** code cell. A connection and access authorization to your Google account is required. Once launched, the browser panel on the left side shows the `je-sample` folder.

![Mount Google Drive](assets/images/googlecolab/image-17.png)

### Set the directory path

1. On the browser panel, right-click the `je-sample` folder and copy its path.
2. Paste the path into the `gdpath` variable and run the cell.

![Set directory path](assets/images/googlecolab/image-18.png)

### Install JAXA Earth API for Python

In the `je-sample` folder, the API package (`jaxa-earth-0.1.3.zip`) is provided.

Run the first three code cells:

1. **First cell** — installs the zip file
2. **Second cell** — imports libraries including the just-installed JAXA Earth library
3. **Third cell** — defines a helper function to get data from JAXA Earth

![Install API](assets/images/googlecolab/image-19.png)

The Google Colab environment is now ready.

## Get Precipitation Rate (Daily)

Data can be retrieved using the following parameters:

| Parameter    | Description       |
|--------------|-------------------|
| `ppu`        | Image resolution  |
| `bbox`       | Area of interest  |
| `collection` | Target dataset ID |
| `sdate`      | Start date        |
| `edate`      | End date          |

Dataset details: <https://data.earth.jaxa.jp/en/datasets/#/id/JAXA.EORC_GSMaP_standard.Gauge.00Z-23Z.v6_daily>

Run the get-data code cell. The output data is stored as the `rain` variable.

![Get precipitation data](assets/images/googlecolab/image-20.png)

To visualize the result, run the visualization code cell.

![Visualize precipitation](assets/images/googlecolab/image-21.png)

Since the color range may be difficult to see, you can adjust the `clim` range values (e.g., `-6` to `2`).

![Adjusted color range](assets/images/googlecolab/image-22.png)

## Get Shortwave Radiation (Daily)

Shortwave radiation can be retrieved with the same code — only change the `collection` variable to the dataset ID.

Dataset details: <https://data.earth.jaxa.jp/en/datasets/#/id/JAXA.JASMES_Aqua.MODIS_swr.v811_global_daily>

- Extent and resolution can be changed by editing the `ppu` and `bbox` variables.

![Get shortwave radiation](assets/images/googlecolab/image-23.png)

- To visualize, reuse the precipitation visualization code with the `radiation` variable.

![Visualize shortwave radiation](assets/images/googlecolab/image-24.png)



---

<!-- START OF FILE: python.en.md -->
# Usage Examples for Python

## Get and show an image

The simplest usage example — get and show an image using all default values:

```python
from jaxa.earth import je

# Get an image
data = je.ImageCollection(ssl_verify=True) \
         .filter_date() \
         .filter_resolution() \
         .filter_bounds() \
         .select() \
         .get_images()

# Process and show an image
img = je.ImageProcess(data) \
        .show_images()
```

![Figure01](assets/images/example/Figure01.png)

To get the raw numpy array and display it:

```python
import matplotlib.pyplot as plt
plt.imshow(img.raster.img[0])
plt.show()
```

![Figure01N](assets/images/example/Figure01N.png)

## Search collection ID and Band

Browse all available datasets at: <https://data.earth.jaxa.jp/en/datasets/>

Use `ImageCollectionList.filter_name()` to search by keywords:

```python
from jaxa.earth import je

# Get all collections and bands
collections, bands = je.ImageCollectionList(ssl_verify=True) \
                       .filter_name()

collection_index = 0
band_index = 0

collection = collections[collection_index]
band = bands[collection_index][band_index]
print(f" - collection : {collection}, band : {band}")
```

## Get and show an image by region of interest

### Set region of interest by bounding box

```python
from jaxa.earth import je

dlim       = ["2021-01-01T00:00:00","2021-01-01T00:00:00"]
ppu        = 5
bbox       = [110, 20, 160, 50]
collection = "NASA.EOSDIS_Terra.MODIS_MOD11C1-LST.daytime.v061_global_half-monthly"
band       = "LST"

data = je.ImageCollection(collection=collection, ssl_verify=True) \
         .filter_date(dlim=dlim) \
         .filter_resolution(ppu=ppu) \
         .filter_bounds(bbox=bbox) \
         .select(band=band) \
         .get_images()

img = je.ImageProcess(data) \
        .show_images()
```

![Figure02_01](assets/images/example/Figure02_01.png)

### Set region of interest by GeoJSON

Create GeoJSON data from [geojson.io](https://geojson.io/) or convert from shapefile in QGIS:

```python
from jaxa.earth import je

dlim       = ["2021-01-01T00:00:00","2021-01-01T00:00:00"]
ppu        = 20
collection = "NASA.EOSDIS_Aqua.MODIS_MYD11C1-LST.daytime.v061_global_half-monthly-normal"
band       = "LST_2012_2021"

geoj_path  = "test.geojson"
geoj       = je.FeatureCollection().read(geoj_path).select()

data = je.ImageCollection(collection=collection, ssl_verify=True) \
         .filter_date(dlim=dlim) \
         .filter_resolution(ppu=ppu) \
         .filter_bounds(geoj=geoj[0]) \
         .select(band=band) \
         .get_images()

img = je.ImageProcess(data) \
        .show_images()
```

![Figure02_02](assets/images/example/Figure02_02.png)

## Get and show a masked image

### Extract range data pixels

Mask GSMaP precipitation data by AW3D elevation range `[0.1, 1000]`:

```python
from jaxa.earth import je

dlim = ["2021-02-01T00:00:00","2021-02-01T00:00:00"]
ppu  = 10
bbox = [110, 20, 160, 50]

# Get data
data_d = je.ImageCollection("JAXA.EORC_GSMaP_standard.Gauge.00Z-23Z.v6_half-monthly-normal", ssl_verify=True) \
           .filter_date(dlim=dlim).filter_resolution(ppu=ppu) \
           .filter_bounds(bbox=bbox).select("PRECIP_2012_2021").get_images()

# Get mask
data_m = je.ImageCollection("JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global", ssl_verify=True) \
           .filter_date(dlim=dlim).filter_resolution(ppu=ppu) \
           .filter_bounds(bbox=bbox).select("DSM").get_images()

# Apply mask
img = je.ImageProcess(data_d) \
        .mask_images(data_m, method_query="range", values=[0.1, 1000]) \
        .show_images()
```

![Figure03_01](assets/images/example/Figure03_01.png)

### Extract values equal data pixels

Mask AW3D elevation by LCCS land cover value `190` (urban areas):

```python
from jaxa.earth import je

dlim = ["2019-01-01T00:00:00","2021-02-01T00:00:00"]
ppu  = 360
bbox = [139.5, 35, 140.5, 36]

data_d = je.ImageCollection("JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global", ssl_verify=True) \
           .filter_date(dlim=dlim).filter_resolution(ppu=ppu) \
           .filter_bounds(bbox=bbox).select("DSM").get_images()

data_m = je.ImageCollection("Copernicus.C3S_PROBA-V_LCCS_global_yearly", ssl_verify=True) \
           .filter_date(dlim=dlim).filter_resolution(ppu=ppu) \
           .filter_bounds(bbox=bbox).select("LCCS").get_images()

img = je.ImageProcess(data_d) \
        .mask_images(data_m, method_query="values_equal", values=[190]) \
        .show_images()
```

![Figure03_02](assets/images/example/Figure03_02.png)

### Extract bits equal data pixels

AW3D DSM (Elevation) masked by AW3D MSK (Mask) using `bits_equal`. All zero bits means effective pixels:

```python
from jaxa.earth import je

dlim       = ["2019-01-01T00:00:00","2021-02-01T00:00:00"]
ppu        = 360
bbox       = [139.5, 35, 140.5, 36]
collection = "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global"

data_d = je.ImageCollection(collection, ssl_verify=True) \
           .filter_date(dlim=dlim).filter_resolution(ppu=ppu) \
           .filter_bounds(bbox=bbox).select("DSM").get_images()

data_m = je.ImageCollection(collection, ssl_verify=True) \
           .filter_date(dlim=dlim).filter_resolution(ppu=ppu) \
           .filter_bounds(bbox=bbox).select("MSK").get_images()

img = je.ImageProcess(data_d) \
        .mask_images(data_m, method_query="bits_equal", values=[0,0,0,0,0,0,0,0]) \
        .show_images()
```

![Figure03_03](assets/images/example/Figure03_03.png)

## Get and show a differential image

Differential image between NDVI (monthly) and NDVI (monthly-normal) using `diff_images`:

```python
from jaxa.earth import je

dlim = ["2021-08-01T00:00:00","2021-08-01T00:00:00"]
bbox = [-180, -90, 180, 90]

# Data
data_d = je.ImageCollection("JAXA.JASMES_Terra.MODIS-Aqua.MODIS_ndvi.v811_global_monthly", ssl_verify=True) \
           .filter_date(dlim=dlim).filter_resolution() \
           .filter_bounds(bbox=bbox).select("ndvi").get_images()

# Reference (normal)
data_r = je.ImageCollection("JAXA.JASMES_Terra.MODIS-Aqua.MODIS_ndvi.v811_global_monthly-normal", ssl_verify=True) \
           .filter_date(dlim=dlim).filter_resolution() \
           .filter_bounds(bbox=bbox).select("ndvi_2012_2021").get_images()

img = je.ImageProcess(data_d) \
        .diff_images(data_r) \
        .show_images()
```

![Figure04](assets/images/example/Figure04.png)

## Get and show a composite image

Composite multiple daily images into one using `calc_temporal_stats`:

```python
from jaxa.earth import je

dlim = ["2021-08-01T00:00:00","2021-08-10T00:00:00"]
bbox = [-180, -90, 180, 90]

data = je.ImageCollection("JAXA.G-Portal_GCOM-W.AMSR2_standard.L3-SMC.daytime.v3_global_daily", ssl_verify=True) \
         .filter_date(dlim=dlim).filter_resolution() \
         .filter_bounds(bbox=bbox).select("SMC").get_images()

img = je.ImageProcess(data) \
        .calc_temporal_stats("mean") \
        .show_images()
```

![Figure05](assets/images/example/Figure05.png)

## Calculate and show timeseries data

Calculate spatial statistics over multiple dates and display as a time series graph:

```python
from jaxa.earth import je

dlim       = ["2021-01-01T00:00:00","2021-12-31T00:00:00"]
bbox       = [120, 20, 150, 50]
ppu        = 10
collection = "JAXA.JASMES_Aqua.MODIS_swr.v811_global_half-monthly-normal"
band       = "swr_2012_2021"

data = je.ImageCollection(collection, ssl_verify=True) \
         .filter_date(dlim=dlim).filter_resolution(ppu=ppu) \
         .filter_bounds(bbox=bbox).select(band).get_images()

img = je.ImageProcess(data) \
        .calc_spatial_stats() \
        .show_spatial_stats()

# Access the timeseries numpy arrays
print(img.timeseries["mean"])
print(img.timeseries["std"])
print(img.timeseries["min"])
print(img.timeseries["max"])
print(img.timeseries["median"])
```

![Figure06](assets/images/example/Figure06.png)


---

<!-- START OF FILE: qgis.en.md -->
# Examples of using the API in QGIS

## Flow of how to use the API in QGIS

1. Launch QGIS on your computer.
2. Click **Browser → XYZ tiles → OpenStreetMap** to fix CRS (Coordinate Reference System) to EPSG3857 and to detect bounding box.
3. Zoom up/down to set your region of interest.
4. Open **Plugins → Python Console**.
5. In Python console, click **Show Editor** icon to open editor.
6. In editor window, make a new script or open your Python script.
7. Execute your Python script by clicking **Run Script** icon.

## Get and show an image in QGIS

Check the location of the installed module:

```bash
pip show jaxa.earth
```

The location will be similar to:

```
C:\users\UserName\appdata\local\packages\...\site-packages
```

If you have not installed the module, add the path to the unzipped folder:

```python
import sys
sys.path.append("C://YOUR-FOLDER-PATH/jaxa-earth-0.1.6")
```

!!! note
    Use `/` instead of `\\` in module path text.

Instead of `show_images`, use `show_images_qgis` in QGIS to acquire raster files.
The raster files are saved in a temporary folder — quit QGIS with saving to keep the data.

```python
import sys
sys.path.append("C://YOUR-FOLDER-PATH/jaxa-earth-0.1.4")

from jaxa.earth import je

# Get an image (ppu and bbox are auto-detected from the QGIS view if omitted)
data = je.ImageCollection(ssl_verify=True) \
         .filter_date() \
         .filter_resolution() \
         .filter_bounds() \
         .select() \
         .get_images()

# Show in QGIS as a raster layer
img = je.ImageProcess(data) \
        .show_images_qgis()
```

![FigureQGIS01](assets/images/example/FigureQGIS01.png)

!!! warning
    `show_images_qgis` is only valid in a QGIS Python Console environment.


---

