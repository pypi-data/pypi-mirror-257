"""
This test module contains unit tests for parsing functionality in the 'wardley_map' package.

The tests in this module are designed to verify the parsing capabilities of the 'wardley_map' package,
specifically ensuring that the parsing functions can accurately interpret and process different
elements of a Wardley Map definition, such as titles, components, and edges.

Functions:
    test_parse_title(): Tests the parsing of map titles from a definition string.
        It creates a map plot by parsing a definition that includes
        only a title and checks if the title is correctly interpreted.

    test_parse_component(): Tests the parsing of individual components from a definition string.
        It creates a map plot by parsing a definition that includes a single component with
        specified coordinates and checks if the component is correctly interpreted and placed on the map.

    test_parse_edge(): Tests the parsing of edges (dependencies) between components from a definition string.
        It creates a map plot by parsing a definition that includes two components and an edge between them,
        verifying if the components and their relationship (edge) are correctly interpreted and represented on the map.

Each test function creates a Wardley Map plot by calling the `create_wardley_map_plot` function
with a map definition string as input, and implicitly checks for errors in the parsing process.
The actual validation of the map plot (e.g., checking if the title, components,
and edges are correctly represented) is not shown in the code snippet
but would typically involve assertions or visual inspection during the test run.
"""

from wardley_map.create_wardley_map import create_wardley_map_plot


def test_parse_title():
    """
    Test the ability to parse the title from a Wardley Map definition string.

    This function tests if the `create_wardley_map_plot` function correctly interprets and handles a map definition that includes only a title. The test passes if no errors occur during the parsing and creation of the map plot, indicating successful title interpretation.
    """

    map_definition = "title Example Map"
    map_plot = create_wardley_map_plot(map_definition)
    if map_plot is not None:
        print("Success")



def test_parse_component():
    """
    Test the parsing of individual components from a Wardley Map definition string.

    This test verifies that the `create_wardley_map_plot` function can accurately parse and incorporate a single component, specified by its name and coordinates, into the map plot. Success is indicated by the absence of errors during parsing and map plot creation, suggesting correct component interpretation and placement.
    """

    map_definition = """
    component Component [0.5, 0.5]
    """
    map_plot = create_wardley_map_plot(map_definition)
    if map_plot is not None:
        print("Success")


def test_parse_edge():
    """
    Test the parsing of edges (dependencies) between components from a Wardley Map definition string.

    This function assesses the ability of the `create_wardley_map_plot` function to parse a definition that includes two components and an edge representing a dependency between them. The test is considered successful if the parsing process completes without errors, implying that both components and their relationship are correctly interpreted and depicted on the map plot.
    """

    map_definition = """
    component A [0.2, 0.2]
    component B [0.8, 0.8]
    component A -> component B
    """
    map_plot = create_wardley_map_plot(map_definition)
    if map_plot is not None:
        print("Success")
