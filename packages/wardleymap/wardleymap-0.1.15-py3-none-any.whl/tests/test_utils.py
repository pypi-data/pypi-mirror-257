# tests/test_utils.py
import pytest
from wardleymap.wardleymap import wardley, create_svg_map, get_owm_map


def test_get_owmmap():
    map_id = "2LcDlz3tAKVRYR4XoA"
    map_text = get_owm_map(map_id)
