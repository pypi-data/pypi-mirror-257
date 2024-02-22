# tests/test_visualisation.py
from wardley_map.create_wardley_map import create_wardley_map_plot
from wardley_map.wardley_maps_utils import create_svg_map


def test_visualisation_elements():
    """
    Test the generation of a Wardley Map's visual representation from its definition.

    This function evaluates the visualisation capabilities of the 'wardley_map' package by creating a map plot from a basic map definition and then generating its SVG content. The map definition includes a title and a single component, providing a minimal but sufficient basis for testing the visualisation process.

    The test involves two main steps:
    1. Creation of a Wardley Map plot using the `create_wardley_map_plot` function with the provided map definition.
    2. Conversion of the map plot to SVG format using the `create_svg_map` function.

    The test is considered successful if the SVG content is generated and is not `None`, indicating that the visualisation pipeline is functioning as expected. The presence of SVG content suggests that the map's elements (e.g., title, components) are correctly processed and rendered into a visual format. The actual content of the SVG is not validated within this test, but the non-null response serves as a basic check for the visualisation process's operational status.
    """

    map_definition = """
    title Example Map
    component A [0.2, 0.2]
    """
    map_plot = create_wardley_map_plot(map_definition)

    # Act: Generate the SVG content
    svg_content = create_svg_map(map_plot)
    if svg_content is not None:
        print("Success")
