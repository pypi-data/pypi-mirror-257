# tests/test_visualisation.py
import pytest
from wardleymap.wardleymap import wardley, create_svg_map


def test_visualisation_elements():
    map_definition = """
    title Example Map
    component A [0.2, 0.2]
    """
    wm, map_plot = wardley(map_definition)

    # Act: Generate the SVG content
    svg_content = create_svg_map(map_plot)
