# tests/test_parsing.py
import pytest
from wardleymap.wardleymap import wardley


def test_parse_title():
    map_definition = "title Example Map"
    wm, map_plot = wardley(map_definition)


def test_parse_component():
    map_definition = """
    component Component [0.5, 0.5]
    """
    wm, map_plot = wardley(map_definition)


def test_parse_edge():
    map_definition = """
    component A [0.2, 0.2]
    component B [0.8, 0.8]
    component A -> component B
    """
    wm, map_plot = wardley(map_definition)
