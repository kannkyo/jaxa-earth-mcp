"""JAXA Earth Python API v0.1.6 reference documentation database."""

JAXA_EARTH_DOCS_V0_1_6 = {
    "version": "0.1.6",
    "overview": (
        "This API package for Python is developed to utilize various Earth observation data "  # noqa
        "held by JAXA. By using this API, you can easily acquire and process data without "  # noqa
        "worrying about specifications, sensors, resolution, etc.\n"
        "je module contains four classes: FeatureCollection, ImageCollectionList, "  # noqa
        "ImageCollection, ImageProcess."
    ),
    "classes": {
        "FeatureCollection": {
            "description": "Reads a feature collection and selects features of GeoJSON data from your computer.",  # noqa
            "attributes": {
                "feature_collection": "dict: Updated after method `read` is executed. Default is None."  # noqa
            },
            "methods": {
                "__init__": "Initialize FeatureCollection instance.",
                "read(path: str)": "Reads input path's GeoJSON data as feature collection.",  # noqa
                "select(keywords: list = [])": "Filter the feature collection data properties by keywords."  # noqa
            },
            "example": """from jaxa.earth import je
geoj_path = "gadm36_JPN_0.geojson"
geoj = je.FeatureCollection().read(geoj_path).select([])"""
        },
        "ImageCollectionList": {
            "description": "Gets and filters collection catalog JSON depending on user input keywords.",  # noqa
            "attributes": {
                "stac_collections": "dict: STAC collections list retrieved from JAXA STAC API."  # noqa
            },
            "methods": {
                "__init__(ssl_verify: bool = True)": "Initialize with SSL verification flag.",  # noqa
                "filter_name(keywords: list = [])": "Filters collection catalog by keywords. Returns (collections, bands)."  # noqa
            },
            "example": """from jaxa.earth import je
keywords = ["LST", "_half-month"]
collections, bands = je.ImageCollectionList(ssl_verify=False).filter_name(keywords=keywords)"""
        },
        "ImageCollection": {
            "description": "Gets selected collection's catalog JSON data from JAXA raster images depending on query.",  # noqa
            "attributes": {
                "stac_date": "Stac class object after filter_date",
                "stac_ppu": "Stac class object after filter_resolution",
                "stac_bounds": "Stac class object after filter_bounds",
                "stac_band": "Stac class object after select"
            },
            "methods": {
                "__init__(collection: str = 'JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global', stac_cog_url: str = None, ssl_verify: bool = True)": "Initialize ImageCollection with target collection ID.",  # noqa
                "filter_date(date: list)": "Filter collection by date list e.g. ['2021-01-01T00:00:00', '2022-01-01T00:00:00'].",  # noqa
                "filter_resolution(resolution: float)": "Filter collection by spatial resolution (meters). Note: Must use filter_date first.",  # noqa
                "filter_bounds(geojson_feature: dict)": "Filter collection by GeoJSON feature spatial boundary. Note: Must use filter_resolution first.",  # noqa
                "select(band: str = None)": "Filter collection catalog by band name. Note: Must use filter_bounds first.",  # noqa
                "get_images()": "Fetch raster images based on configured filters. Returns dictionary or raster dataset."  # noqa
            },
            "example": """from jaxa.earth import je
data_out = je.ImageCollection("JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global")\\
             .filter_date(["2021-01-01T00:00:00","2022-01-01T00:00:00"])\\
             .filter_resolution(20)\\
             .filter_bounds(geoj[0])\\
             .select("DSM")\\
             .get_images()"""
        },
        "ImageProcess": {
            "description": "Processes, visualizes, and calculates spatial statistics on acquired ImageCollection data.",  # noqa
            "attributes": {
                "raster": "Image raster data object",
                "spatial_stats": "Calculated spatial statistics dictionary"
            },
            "methods": {
                "__init__(data_out)": "Initialize ImageProcess with output data from ImageCollection.get_images().",  # noqa
                "show_images()": "Display/plot raster images.",
                "calc_spatial_stats()": "Calculate spatial summary statistics (mean, std, min, max, etc.).",  # noqa
                "show_spatial_stats()": "Display spatial statistics results.",
                "diff_images(ref)": "Take pixel-wise difference relative to reference ImageCollection dataset.",  # noqa
                "mask_images(mask, method_query: str = 'values_equal', values: float = [0, 1])": "Mask raster pixels using mask dataset. Query methods: 'range', 'values_equal', 'bits_equal'."  # noqa
            },
            "example": """from jaxa.earth import je
img = je.ImageProcess(data_out)\\
        .show_images()\\
        .calc_spatial_stats()\\
        .show_spatial_stats()"""
        }
    },
    "popular_collections": [
        {
            "id": "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global",
            "name": "ALOS World 3D - 30m (AW3D30)",
            "bands": ["DSM"],
            "description": "Global 30m Digital Surface Model"
        },
        {
            "id": "JAXA.EORC_ALOS-2.PALSAR-2.v2.1.0_global",
            "name": "ALOS-2 PALSAR-2 Global Mosaic",
            "bands": ["HH", "HV"],
            "description": "L-band Synthetic Aperture Radar (SAR) mosaic"
        },
        {
            "id": "JAXA.EORC_GCOM-C.SGLI_LST_half-month",
            "name": "GCOM-C SGLI Land Surface Temperature",
            "bands": ["LST"],
            "description": "15-day composite Land Surface Temperature"
        },
        {
            "id": "JAXA.EORC_GSMaP.v8_global",
            "name": "Global Satellite Mapping of Precipitation (GSMaP)",
            "bands": ["hourlyGPM"],
            "description": "Global precipitation rate estimates"
        }
    ]
}

def get_reference_doc(class_name: str = None) -> str:
    """Return documentation for specified class or full overview."""
    if not class_name or class_name.lower() == "all":
        output = [f"# JAXA Earth Python API Documentation (v{JAXA_EARTH_DOCS_V0_1_6['version']})\n"]  # noqa
        output.append(JAXA_EARTH_DOCS_V0_1_6["overview"])
        output.append("\n## Available Classes:\n")
        for cls_name, info in JAXA_EARTH_DOCS_V0_1_6["classes"].items():
            output.append(f"### `jaxa.earth.je.{cls_name}`")
            output.append(f"{info['description']}\n")
            output.append("Methods:")
            for m, m_desc in info["methods"].items():
                output.append(f"- `{m}`: {m_desc}")
            output.append("\nExample:")
            output.append(f"```python\n{info['example']}\n```\n")
        return "\n".join(output)
    
    cls_dict = {k.lower(): k for k in JAXA_EARTH_DOCS_V0_1_6["classes"].keys()}
    target_cls = cls_dict.get(class_name.lower())
    if target_cls:
        info = JAXA_EARTH_DOCS_V0_1_6["classes"][target_cls]
        res = [f"# Class: `jaxa.earth.je.{target_cls}`\n", info["description"], "\n### Attributes:"]  # noqa
        for attr, desc in info["attributes"].items():
            res.append(f"- `{attr}`: {desc}")
        res.append("\n### Methods:")
        for m, m_desc in info["methods"].items():
            res.append(f"- `{m}`: {m_desc}")
        res.append("\n### Example:")
        res.append(f"```python\n{info['example']}\n```")
        return "\n".join(res)
    else:
        return f"Unknown class '{class_name}'. Available classes: {list(JAXA_EARTH_DOCS_V0_1_6['classes'].keys())}"  # noqa
