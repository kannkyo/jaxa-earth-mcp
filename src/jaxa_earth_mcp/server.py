"""MCP Server for JAXA Earth Python API (jaxa.earth.je)."""

from typing import List, Optional, Dict, Any
import json

try:
    from fastmcp import FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

from jaxa_earth_mcp.docs_reference import JAXA_EARTH_DOCS_V0_1_6, get_reference_doc

# Initialize FastMCP Server
mcp = FastMCP("jaxa-earth-mcp")

@mcp.tool()
def get_api_documentation(class_name: str = "all") -> str:
    """Retrieve official documentation and code examples for JAXA Earth Python API (jaxa.earth.je v0.1.6).
    
    Args:
        class_name: Name of the class to get documentation for ('FeatureCollection', 'ImageCollectionList', 'ImageCollection', 'ImageProcess', or 'all').
    """
    return get_reference_doc(class_name)

@mcp.tool()
def list_collections(keywords: Optional[List[str]] = None) -> str:
    """List or filter popular and available satellite datasets on JAXA Earth Platform.
    
    Args:
        keywords: Optional list of keyword strings to filter collections (e.g. ['ALOS', 'LST', 'PRISM']).
    """
    try:
        from jaxa.earth import je
        col_list, band_list = je.ImageCollectionList(ssl_verify=False).filter_name(keywords=keywords or [])
        res = {
            "source": "JAXA STAC Live API",
            "collections_found": len(col_list),
            "data": [{"collection": c, "band": b} for c, b in zip(col_list, band_list)]
        }
        return json.dumps(res, indent=2, ensure_ascii=False)
    except Exception as e:
        # Fallback to internal curated list if live call fails or jaxa.earth not installed
        popular = JAXA_EARTH_DOCS_V0_1_6["popular_collections"]
        if keywords:
            filtered = [
                c for c in popular
                if any(kw.lower() in c["id"].lower() or kw.lower() in c["name"].lower() for kwstr in keywords for kw in [kwstr])
            ]
        else:
            filtered = popular
        
        res = {
            "source": "Curated JAXA Earth Registry (Live API offline or fallback)",
            "note": str(e),
            "collections": filtered
        }
        return json.dumps(res, indent=2, ensure_ascii=False)

@mcp.tool()
def generate_jaxa_python_script(
    collection: str = "JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global",
    start_date: str = "2021-01-01T00:00:00",
    end_date: str = "2022-01-01T00:00:00",
    resolution: float = 20.0,
    geojson_path: str = "gadm36_JPN_0.geojson",
    select_band: str = "DSM",
    calc_stats: bool = True
) -> str:
    """Generate verified, executable Python script using jaxa.earth.je API to fetch and process satellite data.
    
    Args:
        collection: JAXA Earth collection ID.
        start_date: ISO 8601 start date (YYYY-MM-DDTHH:MM:SS).
        end_date: ISO 8601 end date (YYYY-MM-DDTHH:MM:SS).
        resolution: Spatial resolution filter in meters.
        geojson_path: File path to GeoJSON boundary file.
        select_band: Target band name (e.g. 'DSM', 'LST', 'HH').
        calc_stats: Whether to calculate spatial statistics in the script.
    """
    script = f'''# Generated JAXA Earth Python API Script (jaxa.earth.je v0.1.6)
from jaxa.earth import je

# 1. Load spatial boundary from GeoJSON
geoj_path = "{geojson_path}"
geoj = je.FeatureCollection().read(geoj_path).select([])

# 2. Query & fetch raster image collection
# Note method call chain order requirement: filter_date -> filter_resolution -> filter_bounds -> select -> get_images
data_out = (
    je.ImageCollection("{collection}")
    .filter_date(["{start_date}", "{end_date}"])
    .filter_resolution({resolution})
    .filter_bounds(geoj[0])
    .select("{select_band}")
    .get_images()
)

# 3. Process and display raster images
img_proc = je.ImageProcess(data_out).show_images()
'''
    if calc_stats:
        script += '''
# 4. Calculate spatial statistics (mean, std, min, max, etc.)
img_proc = img_proc.calc_spatial_stats().show_spatial_stats()
'''
    return script

@mcp.resource("jaxa://docs/api")
def api_docs_resource() -> str:
    """Resource providing full JAXA Earth Python API v0.1.6 reference."""
    return get_reference_doc("all")

@mcp.resource("jaxa://collections/popular")
def popular_collections_resource() -> str:
    """Resource listing popular JAXA satellite datasets."""
    return json.dumps(JAXA_EARTH_DOCS_V0_1_6["popular_collections"], indent=2)

@mcp.prompt()
def satellite_data_analysis(query: str) -> str:
    """Create prompt instructions for JAXA satellite data analysis."""
    return f"""You are an expert Earth Observation data scientist using the JAXA Earth Python API (`jaxa.earth.je`).
User request: "{query}"

Please provide a complete Python solution following the JAXA Earth API (v0.1.6) conventions:
1. Use `jaxa.earth.je` module.
2. Maintain strict method call ordering for ImageCollection:
   `ImageCollection(col).filter_date(...).filter_resolution(...).filter_bounds(...).select(...).get_images()`
3. Process raster outputs using `ImageProcess`.
"""

def run_server():
    """Run the FastMCP server."""
    mcp.run()

if __name__ == "__main__":
    run_server()
