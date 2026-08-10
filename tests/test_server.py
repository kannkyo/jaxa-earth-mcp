"""Tests for jaxa_earth_mcp.server tools."""

import json

from jaxa_earth_mcp.server import (generate_jaxa_python_script,
                                   get_api_documentation, list_collections)


def test_tool_get_api_documentation():
    doc = get_api_documentation("ImageCollection")
    assert "ImageCollection" in doc
    assert "filter_date" in doc


def test_tool_list_collections():
    res_str = list_collections(keywords=["ALOS"])
    res = json.loads(res_str)
    assert "collections" in res or "data" in res


def test_tool_generate_jaxa_python_script():
    script = generate_jaxa_python_script(
        collection="JAXA.EORC_ALOS.PRISM_AW3D30.v3.2_global",
        start_date="2021-01-01T00:00:00",
        end_date="2022-01-01T00:00:00",
        resolution=20.0,
        select_band="DSM"
    )
    assert "from jaxa.earth import je" in script
    assert ".filter_date([\"2021-01-01T00:00:00\", \"2022-01-01T00:00:00\"])" in script  # noqa
    assert ".filter_resolution(20.0)" in script
    assert ".select(\"DSM\")" in script
