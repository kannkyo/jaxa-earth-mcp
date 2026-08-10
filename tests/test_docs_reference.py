"""Tests for jaxa_earth_mcp.docs_reference module."""

from jaxa_earth_mcp.docs_reference import JAXA_EARTH_DOCS_V0_1_6, get_reference_doc

def test_docs_structure():
    assert JAXA_EARTH_DOCS_V0_1_6["version"] == "0.1.6"
    assert "FeatureCollection" in JAXA_EARTH_DOCS_V0_1_6["classes"]
    assert "ImageCollection" in JAXA_EARTH_DOCS_V0_1_6["classes"]

def test_get_reference_doc_all():
    doc = get_reference_doc("all")
    assert "JAXA Earth Python API Documentation" in doc
    assert "FeatureCollection" in doc
    assert "ImageCollection" in doc

def test_get_reference_doc_single_class():
    doc = get_reference_doc("FeatureCollection")
    assert "Class: `jaxa.earth.je.FeatureCollection`" in doc
    assert "read(path: str)" in doc

def test_get_reference_doc_unknown_class():
    doc = get_reference_doc("UnknownClass")
    assert "Unknown class" in doc
