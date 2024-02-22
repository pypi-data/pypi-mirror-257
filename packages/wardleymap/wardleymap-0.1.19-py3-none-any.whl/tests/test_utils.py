# tests/test_utils.py
from wardley_map.wardley_maps_utils import get_owm_map


def test_get_owmmap():
    """
    Test the retrieval of a Wardley Map text representation using its unique identifier.

    This function tests the `get_owm_map` utility from the `wardley_map.wardley_maps_utils` module, which is designed to fetch the text representation of a Wardley Map given its unique map ID. The test provides a hardcoded map ID, retrieves the map text using the `get_owm_map` function, and prints the result.

    The primary purpose of this test is to verify the functionality and reliability of the map retrieval process. It checks whether the `get_owm_map` function can successfully connect to the data source, query a map by its ID, and return its text representation. The success of the test is determined by the absence of errors during the retrieval process and the correctness of the returned map text, which is not explicitly checked in this code snippet but can be verified through manual inspection or additional assertions.
    """

    map_id = "2LcDlz3tAKVRYR4XoA"
    map_text = get_owm_map(map_id)
    print(map_text)
