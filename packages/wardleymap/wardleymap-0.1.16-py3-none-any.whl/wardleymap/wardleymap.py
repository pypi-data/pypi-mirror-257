"""
Wardley Map Parser and Visualiser

This module provides the WardleyMap class, designed to parse, interpret,
and manage the data of Wardley Maps from their textual representation in Open Wardley Map (OWM) syntax.
It supports extracting components, anchors, pipelines, notes, and more from a given map syntax or map ID,
allowing for further analysis and visualization of the map's content.
Additionally, the class can fetch map data from a remote source using a map ID.

The WardleyMap class offers methods to retrieve detailed information about the map's components,
including their evolution stages, visibility, and relationships.
It also includes functionality to identify and report potential issues or unsupported features in the map syntax.

Dependencies:
    - json: For parsing JSON data.
    - re: For regular expression operations.
    - requests: For making HTTP requests to fetch map data from remote sources.

Example usage:
    owm_syntax = "<Your OWM syntax here>"
    wardley_map = WardleyMap(owm_syntax)
    components = wardley_map.getComponents()
    print(components)

Note:
    This module is intended for educational and informational purposes.
    Ensure you have the necessary permissions to fetch and use map data from remote sources.
"""

import matplotlib
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re, requests, json
from io import BytesIO


class WardleyMap:
    """
    Represents a Wardley Map parsed from a given Wardley Map Syntax (OWM) string or a map ID.

    This class provides functionalities to parse various components of a Wardley Map
    including nodes (components and anchors), edges, pipelines, evolutions,
    and notes from the OWM syntax. It also supports fetching map data
    from a remote source using a map ID.

    Attributes:
        title (str): The title of the Wardley Map.
        anchors (list): A list of anchors in the map.
        nodes (dict): A dictionary of nodes in the map, keyed by node title.
        edges (list): A list of edges (relationships) between nodes.
        bluelines (list): A list of blueline relationships between nodes.
        evolutions (dict): A dictionary containing evolution stages of components.
        evolves (dict): A dictionary containing evolve relationships between nodes.
        pipelines (dict): A dictionary of pipelines in the map.
        annotations (list): A list of annotations in the map.
        notes (list): A list of notes associated with the map.
        style (str): The visual style of the map.
        warnings (list): A list of warnings generated during parsing.
        components (list): A list of components parsed from the map.
        component (dict): Details of a single component when searched by name.
    """

    # Developed using https://regex101.com/
    _coords_regexs = "\\[\\s*([\\d\\.-]+)\\s*,\\s*([\\d\\.-]+)\\s*\\]"

    # _node_regex = re.compile(r"^(\w+) ([a-zA-Z0-9_.,/&' +)(?-]+)\s+{COORDS}(\s+label\s+{COORDS})*".format(COORDS=_coords_regexs))
    _node_regex = re.compile(
        r"^(\w+) (?:.*?//.*?)?([a-zA-Z0-9_.,/&' +)(?-]+?)\s+{COORDS}(\s+label\s+{COORDS})*".format(
            COORDS=_coords_regexs
        )
    )

    # _evolve_regex = re.compile(r"^evolve ([\w \/',)(-]+)\s+([\d\.-]+)(\s+label\s+{COORDS})*".format(COORDS=_coords_regexs))
    _evolve_regex = re.compile(
        r"^evolve (?:.*?//.*?)?([\w \/',)(-]+?)\s+([\d\.-]+)(\s+label\s+{COORDS})*".format(
            COORDS=_coords_regexs
        )
    )

    # _pipeline_regex = re.compile(r"^pipeline ([a-zA-Z0-9_.,/&' )(?-]+)\s+\[\s*([\d\.]+)\s*,\s*([\d\.]+)\s*\]$")
    _pipeline_regex = re.compile(
        r"^pipeline ([a-zA-Z0-9_.,/&' )(?-]+?)(?:\s*//.*)?\s+\[\s*([\d\.]+)\s*,\s*([\d\.]+)\s*\]$"
    )

    # _note_regex = re.compile(r"^(\w+) ([\S ]+)\s+{COORDS}\s*".format(COORDS=_coords_regexs))
    _note_regex = re.compile(
        r"^(\w+) (?:.*?//.*?)?([\S ]+?)\s+{COORDS}\s*".format(COORDS=_coords_regexs)
    )

    def __init__(self, owm: str):
        """
        Initializes a WardleyMap object either from a map ID or OWM syntax string.

        If the provided string is recognized as a map ID,the map data is fetched from a remote source.
        Otherwise, the string is treated as the OWM syntax of the map and parsed accordingly.

        Parameters:
            owm (str): A string representing either the map ID or the OWM syntax of a Wardley Map.
        """

        # Defaults:
        self.title = None
        self.nodes = {}
        self.edges = []
        self.bluelines = []
        self.evolutions = {}
        self.evolves = {}
        self.pipelines = {}
        self.annotations = []
        self.annotation = {}
        self.notes = []
        self.style = None
        self.warnings = []
        self.components = []
        self.anchors = []
        self.component = None


        if self.is_map_id(owm):
            self.map_id = owm
            self.owm = self.fetch_map_text()
        else:
            self.map_id = None
            self.owm = owm

        # Fetch the Wadley Map text from maps.wardleymaps.ai
        #self.fetch_map_data()

        # And load:
        for cl in owm.splitlines():
            cl = cl.strip()
            if not cl:
                continue

            if cl.startswith("#"):
                # Skip comments...
                continue

            if cl.startswith("//"):
                # Skip comments...
                continue

            if cl.startswith("annotation "):
                warning_message = "Displaying annotation not supported yet"
                if warning_message not in self.warnings:
                    self.warnings.append(warning_message)
                continue

            if cl.startswith("annotations "):
                warning_message = "Displaying annotations not supported yet"
                if warning_message not in self.warnings:
                    self.warnings.append(warning_message)
                continue

            if cl.startswith("market "):
                warning_message = "Displaying market not supported yet"
                if warning_message not in self.warnings:
                    self.warnings.append(warning_message)
                continue

            if cl.startswith("pipeline "):
                match = self._pipeline_regex.search(cl)
                if match is not None:
                    matches = match.groups()
                    pipeline = {
                            "title": matches[0],
                            "start_mat": float(matches[1]),
                            "end_mat": float(matches[2]),
                    }

                    # And store it:
                    self.pipelines[matches[0]] = pipeline
                    continue

                self.warnings.append(f"Could not parse pipeline: {cl}")

            if cl.startswith("evolution "):
                warning_message = "Displaying evolution not supported yet"
                if warning_message not in self.warnings:
                    self.warnings.append(warning_message)
                    continue

            if cl.startswith("title "):
                self.title = cl.split(" ", maxsplit=1)[1]
                continue

            if cl.startswith("style "):
                self.style = cl.split(" ", maxsplit=1)[1]
                continue

            if cl.startswith('anchor '):
                # Use RegEx to split into fields:
                match = self._node_regex.search(cl)
                if match is not None:
                    matches = match.groups()
                    node = {
                            'type': matches[0],
                            'title': matches[1],
                            'vis': float(matches[2]),
                            'mat': float(matches[3])
                    }
                    # Handle label position adjustments:
                    if matches[4]:
                        node['label_x'] = float(matches[5])
                        node['label_y'] = float(matches[6])
                    else:
                        # Default to a small additional offset:
                        node['label_x'] = 2
                        node['label_y'] = 2
                    # And store it:
                    self.nodes[node['title']] = node
                else:
                    self.warnings.append(f"Could not parse anchor: {cl}")

            if cl.startswith('component '):
                # Use RegEx to split into fields:
                match = self._node_regex.search(cl)
                if match is not None:
                    matches = match.groups()
                    node = {
                            'type': matches[0],
                            'title': matches[1],
                            'vis': float(matches[2]),
                            'mat': float(matches[3])
                    }
                    # Handle label position adjustments:
                    if matches[4]:
                        node['label_x'] = float(matches[5])
                        node['label_y'] = float(matches[6])
                    else:
                        # Default to a small additional offset:
                        node['label_x'] = 2
                        node['label_y'] = 2
                    # And store it:
                    self.nodes[node['title']] = node
                else:
                    self.warnings.append(f"Could not parse component line: {cl}")

            if cl.startswith("evolve "):
                match = self._evolve_regex.search(cl)
                if match is not None:
                    matches = match.groups()
                    evolve = {"title": matches[0], "mat": float(matches[1])}
                    # Handle label position adjustments:
                    if matches[3] is not None:
                        evolve["label_x"] = float(matches[3])
                    else:
                        evolve["label_x"] = 2

                    if matches[4] is not None:
                        evolve["label_y"] = float(matches[4])
                    else:
                        evolve["label_y"] = 2

                    # And store it:
                    self.evolves[matches[0]] = evolve
                    continue

                self.warnings.append(f"Could not parse evolve line: {cl}")

            if "->" in cl:
                edge_parts = cl.split("->")
                if len(edge_parts) != 2:
                    self.warnings.append(
                            f"Unexpected format for edge definition: {cl}. Skipping this edge."
                    )
                    continue
                n_from, n_to = edge_parts
                self.edges.append([n_from.strip(), n_to.strip()])

            if "+<>" in cl:
                edge_parts = cl.split("+<>")
                if len(edge_parts) != 2:
                    self.warnings.append(
                            f"Unexpected format for blueline definition: {cl}. Skipping this edge."
                    )
                    continue
                n_from, n_to = edge_parts
                self.bluelines.append([n_from.strip(), n_to.strip()])
                continue

            if cl.startswith("note"):
                match = self._note_regex.search(cl)
                if match is not None:
                    matches = match.groups()
                    note = {
                            "text": matches[1],
                    }
                    # Handle text position adjustments:
                    if matches[2]:
                        note["vis"] = float(matches[2])
                        note["mat"] = float(matches[3])
                    else:
                        # Default to a small additional offset:
                        note["vis"] = 0.2
                        note["mat"] = 0.2
                    # And store it:
                    self.notes.append(note)

                self.warnings.append(f"Could not parse note line: {cl}")
            # Warn about lines we can't handle?
            self.warnings.append(f"Could not parse line: {cl}")

        self.warnings = list(set(self.warnings))
        print("Initialization complete.")

    def is_map_id(self, val):
        """
        Check if a value is a valid map ID based on its format.
        :param val: The value to check.
        :type val: str
        :return: True if the value is a valid map ID, False otherwise.
        """
        return len(val) == 18

    def fetch_map_text(self):
        """
        Fetches the map data using the Wardley Mapping AI API.
        """
        url = f"https://maps.wardleymaps.ai/v2/maps/fetch?id={self.map_id}"
        response = requests.get(url, timeout=1)

        if response.status_code == 200:
            mapdata = response.json()
            self.owm = mapdata['text']
        else:
            self.owm = None
        return self.owm

    def get_warnings(self):
        """
        Parses the Wardley Map syntax to identify and return any warnings generated during parsing.

        Warnings may include unrecognized lines, unsupported features, or errors in the map syntax.

        Returns:
            list: A list of warning messages.
        """

        if self.owm is None:
            raise ValueError(
                    "Map is not initialized. Please check if the map ID is correct.")

        self.warnings = []
        # Parse the map:
        for cl in self.owm.splitlines():
            cl = cl.strip()
            if not cl:
                continue

            if cl.startswith('#'):
                # Skip comments...
                continue

            if cl.startswith('//'):
                # Skip comments...
                continue

            if cl.startswith('annotation '):
                warning_message = "Displaying annotation not supported yet"
                if warning_message not in self.warnings:
                    self.warnings.append(warning_message)
                continue

            if cl.startswith('annotations '):
                warning_message = "Displaying annotations not supported yet"
                if warning_message not in self.warnings:
                    self.warnings.append(warning_message)
                continue

            if cl.startswith('market '):
                warning_message = "Displaying market not supported yet"
                if warning_message not in self.warnings:
                    self.warnings.append(warning_message)
                continue

            if cl.startswith('pipeline '):
                match = self._pipeline_regex.search(cl)
                if match is not None:
                    matches = match.groups()
                    pipeline = {
                            'title': matches[0],
                            'start_mat': float(matches[1]),
                            'end_mat': float(matches[2]),
                    }

                    # And store it:
                    self.pipelines[matches[0]] = pipeline
                    continue

                self.warnings.append(f"Could not parse pipeline: {cl}")

            if cl.startswith('title '):
                self.title = cl.split(' ', maxsplit=1)[1]
                continue

            if cl.startswith('style '):
                self.style = cl.split(' ', maxsplit=1)[1]
                continue

            if cl.startswith('anchor ') or cl.startswith('component '):
                # Use RegEx to split into fields:
                match = self._node_regex.search(cl)
                if match is not None:
                    matches = match.groups()
                    node = {
                            'type': matches[0],
                            'title': matches[1],
                            'vis': float(matches[2]),
                            'mat': float(matches[3])
                    }
                    # Handle label position adjustments:
                    if matches[4]:
                        node['label_x'] = float(matches[5])
                        node['label_y'] = float(matches[6])
                    else:
                        # Default to a small additional offset:
                        node['label_x'] = 2
                        node['label_y'] = 2
                    # And store it:
                    self.nodes[node['title']] = node
                else:
                    self.warnings.append(f"Could not parse component line: {cl}")

            if cl.startswith('evolve '):
                match = self._evolve_regex.search(cl)
                if match is not None:
                    matches = match.groups()
                    evolve = {'title': matches[0], 'mat': float(matches[1])}
                    # Handle label position adjustments:
                    if matches[3] is not None:
                        evolve['label_x'] = float(matches[3])
                    else:
                        evolve['label_x'] = 2

                    if matches[4] is not None:
                        evolve['label_y'] = float(matches[4])
                    else:
                        evolve['label_y'] = 2

                    # And store it:
                    self.evolves[matches[0]] = evolve
                    continue

                self.warnings.append(f"Could not parse evolve line: {cl}")

            if "->" in cl:
                edge_parts = cl.split('->')
                if len(edge_parts) != 2:
                    self.warnings.append(
                            f"Unexpected format for edge definition: {cl}. Skipping this edge."
                    )
                    continue
                n_from, n_to = edge_parts
                self.edges.append([n_from.strip(), n_to.strip()])

            if "+<>" in cl:
                edge_parts = cl.split('+<>')
                if len(edge_parts) != 2:
                    self.warnings.append(
                            f"Unexpected format for blueline definition: {cl}. Skipping this edge."
                    )
                    continue
                n_from, n_to = edge_parts
                self.bluelines.append([n_from.strip(), n_to.strip()])
                continue

            if cl.startswith('note'):
                match = self._note_regex.search(cl)
                if match is not None:
                    matches = match.groups()
                    note = {
                            'text': matches[1],
                    }
                    # Handle text position adjustments:
                    if matches[2]:
                        note['vis'] = float(matches[2])
                        note['mat'] = float(matches[3])
                    else:
                        # Default to a small additional offset:
                        note['vis'] = .2
                        note['mat'] = .2
                    # And store it:
                    self.notes.append(note)

                self.warnings.append(f"Could not parse note line: {cl}")
            self.warnings.append(f"Could not parse line: {cl}")

        self.warnings = list(set(self.warnings))
        return {
                'warnings': self.warnings,
                #'text': self.owm
        }


    def get_notes(self):
        """
        Extracts and returns notes from the Wardley Map syntax.

        Returns:
            list: A list of dictionaries, each representing a note with its content and position.
        """
        if self.owm is None:
            raise ValueError(
                    "Map is not initialized. Please check if the map ID is correct.")

        self.notes = []
        lines = self.owm.strip().split("\n")
        for line in lines:
            if line.startswith("note"):
                note = line[line.find(' ') + 1:line.find('[')].strip()
                pos_index = line.find("[")
                self.swap_xy(line) if pos_index != -1 else ""
                self.notes.append({'note': note})
        return self.notes


    def get_annotations(self):
        """
        Extracts and returns annotations from the Wardley Map syntax.

        Returns:
            list: A list of dictionaries,
            each representing an annotation with its number and content.
        """
        if self.owm is None:
            raise ValueError(
                    "Map is not initialized. Please check if the map ID is correct.")

        self.annotations = []
        lines = self.owm.strip().split("\n")
        for line in lines:
            if line.startswith("annotation"):
                self.swap_xy(line)
                number = re.findall(r'\d+', line)
                annotation = line[line.index(']') + 1:].lstrip()
                self.annotations.append({
                        "number": number[0],
                        "annotation": annotation
                })
        self.annotations = [
                i for n, i in enumerate(self.annotations)
                if i not in self.annotations[n + 1:]
        ]  # Remove duplicates
        return self.annotations


    def get_components(self):
        """
        Extracts and returns the components from the Wardley Map syntax.

        Returns:
            list: A list of dictionaries, each representing a component with its name,
            evolution stage, visibility, and description.
        """
        if self.owm is None:
            raise ValueError(
                    "Map is not initialized. Please check if the map ID is correct.")

        self.components = []
        lines = self.owm.strip().split("\n")
        for line in lines:
            if line.startswith("component"):
                stage = ""
                pos_index = line.find("[")
                if pos_index != -1:
                    new_c_xy = self.swap_xy(line)
                    number = json.loads(new_c_xy)
                    if 0 <= number[0] <= 0.17:
                        stage = "genesis"
                    if 0.18 <= number[0] <= 0.39:
                        stage = "custom"
                    if 0.40 <= number[0] <= 0.69:
                        stage = "product"
                    if 0.70 <= number[0] <= 1.0:
                        stage = "commodity"
                    stage = ""
                    if 0 <= number[1] <= 0.20:
                        visibility = "low"
                    if 0.21 <= number[1] <= 0.70:
                        visibility = "medium"
                    if 0.71 <= number[1] <= 1.0:
                        visibility = "high"
                    visibility = ""
                else:
                    new_c_xy = ""
                name = line.split('[')[0].split(' ', 1)[1].strip()
                self.components.append({
                        'name': name,
                        'evolution': stage,
                        'visibility': visibility,
                        'description': ''
                })
        return self.components


    def get_anchors(self):
        """
        Extracts and returns all the anchors from the Wardley Map syntax.

        Each anchor is represented as a dictionary containing its name, evolution stage, and visibility.

        Returns:
            list[dict]: A list of dictionaries, each representing an anchor with its details.
        """

        if self.owm is None:
            raise ValueError(
                    "Map is not initialized. Please check if the map ID is correct.")

        self.anchors = []
        lines = self.owm.strip().split("\n")
        for line in lines:
            if line.startswith("anchor"):
                stage = ""
                pos_index = line.find("[")
                if pos_index != -1:
                    new_c_xy = self.swap_xy(line)
                    number = json.loads(new_c_xy)
                    if 0 <= number[0] <= 0.17:
                        stage = "genesis"
                    if 0.18 <= number[0] <= 0.39:
                        stage = "custom"
                    if 0.40 <= number[0] <= 0.69:
                        stage = "product"
                    if 0.70 <= number[0] <= 1.0:
                        stage = "commodity"
                    stage = ""
                    if 0 <= number[1] <= 0.20:
                        visibility = "low"
                    if 0.21 <= number[1] <= 0.70:
                        visibility = "medium"
                    if 0.71 <= number[1] <= 1.0:
                        visibility = "high"
                    visibility = ""
                else:
                    new_c_xy = ""
                anchor = line.split('[')[0].split(' ', 1)[1].strip()
                self.anchors.append({
                        'name': anchor,
                        'evolution': stage,
                        'visibility': visibility
                })
        return self.anchors


    def get_pipelines(self):
        """
        Extracts and returns all the pipelines from the Wardley Map syntax.

        Each pipeline is represented as a dictionary containing its name, evolution stage, and visibility.

        Returns:
            list[dict]: A list of dictionaries, each representing a pipeline with its details.
        """

        if self.owm is None:
            raise ValueError(
                    "Map is not initialized. Please check if the map ID is correct.")

        self.pipelines = []
        lines = self.owm.strip().split("\n")
        for line in lines:
            if line.startswith("pipeline"):
                stage = ""
                pos_index = line.find("[")
                if pos_index != -1:

                    new_c_xy = self.swap_xy(line)
                    number = json.loads(new_c_xy)
                    if 0 <= number[0] <= 0.17:
                        stage = "genesis"
                    if 0.18 <= number[0] <= 0.39:
                        stage = "custom"
                    if 0.40 <= number[0] <= 0.69:
                        stage = "product"
                    if 0.70 <= number[0] <= 1.0:
                        stage = "commodity"
                    stage = ""
                    if 0 <= number[1] <= 0.20:
                        visibility = "low"
                    if 0.21 <= number[1] <= 0.70:
                        visibility = "medium"
                    if 0.71 <= number[1] <= 1.0:
                        visibility = "high"
                    visibility = ""
                else:
                    new_c_xy = ""
                pipeline = line.split('[')[0].split(' ', 1)[1].strip()
                self.pipelines.append({
                        'name': pipeline,
                        'evolution': stage,
                        'visibility': visibility
                })
        return self.pipelines


    def get_component(self, component_name):
        """
        Retrieves the details of a specific component by its name.

        Parameters:
            component_name (str): The name of the component to retrieve.

        Returns:
            dict: A dictionary containing the details of the specified component, including its name, evolution stage, visibility, and description. Returns None if the component is not found.
        """

        if self.owm is None:
            raise ValueError(
                    "Map is not initialized. Please check if the map ID is correct.")

        self.component = None
        lines = self.owm.strip().split("\n")
        for line in lines:
            if f"component {component_name}" in line:
                stage = ""
                pos_index = line.find("[")
                if pos_index != -1:
                    new_c_xy = self.swap_xy(line)
                    number = json.loads(new_c_xy)
                    if 0 <= number[0] <= 0.17:
                        stage = "genesis"
                    if 0.18 <= number[0] <= 0.39:
                        stage = "custom"
                    if 0.40 <= number[0] <= 0.69:
                        stage = "product"
                    if 0.70 <= number[0] <= 1.0:
                        stage = "commodity"
                    stage = ""
                    if 0 <= number[1] <= 0.20:
                        visibility = "low"
                    if 0.21 <= number[1] <= 0.70:
                        visibility = "medium"
                    if 0.71 <= number[1] <= 1.0:
                        visibility = "high"
                    visibility = ""
                else:
                    new_c_xy = ""
                self.component = {
                        'name': line.split(' ')[1],
                        'evolution': stage,
                        'visibility': visibility,
                        'description': ''
                }
                break  # Exit the loop as soon as we've found our component
        return self.component


    def swap_xy(self, xy):
        """
        Swaps the x and y coordinates in a string representation of a coordinate pair.

        Parameters:
            xy (str): A string containing the coordinate pair.

        Returns:
            str: The string with swapped coordinates.
        """
        new_xy = re.findall("\\[(.*?)\\]", xy)
        if new_xy:
            match = new_xy[0]
            match = match.split(sep=",")
            match = match[::-1]
            new_xy = '[' + match[0].strip() + ',' + match[1] + ']'
            return new_xy

        new_xy = ""
        return new_xy


    def get_map_text(self):
        """
        Returns the original Wardley Map syntax as a string.

        Returns:
            str: The OWM syntax of the Wardley Map.
        """
        if self.owm is None:
            raise ValueError(
                    "Map is not initialized. Please check if the map ID is correct.")
        return self.owm


    def search_component(self, search_term):
        """
        Search for components in the Wardley Map by a search term.

        :param search_term: The term to search for in component names
        :type search_term: str
        :return: A list of components that match the search term
        """
        if self.owm is None:
            raise ValueError(
                    "Map is not initialized. Please check if the map ID is correct.")

        # Ensure components are parsed and up to date
        self.get_components()

        # Perform case-insensitive search
        search_term = search_term.lower()
        found_components = [
                component for component in self.components
                if search_term in component['name'].lower()
                or search_term in component.get('evolution', '').lower()
                or search_term in component.get('visibility', '').lower()
        ]

        return found_components



def wardley(map):
    """
    Parses the provided OWM syntax to create a WardleyMap object and generates a matplotlib figure representing the map.

    Args:
        map (str): The map definition in OWM syntax.

    Returns:
        tuple: A tuple containing the WardleyMap object and the matplotlib figure.
    """

    # Parse the OWM syntax:
    wm = WardleyMap(map)

    # Now plot, with styles:
    fig = None
    figsize = (10, 7)
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)

    if wm.style is None:
        wm.style = "wardley"

    if wm.style == "wardley":
        # Use a monospaced font:
        matplotlib.rcParams["font.family"] = "monospace"
        matplotlib.rcParams["font.size"] = 6
        # Set up the default plot:
        fig, ax = plt.subplots(figsize=figsize)
        # Add the gradient background
        norm = matplotlib.colors.Normalize(0, 1)
        colors = [[norm(0.0), "white"], [norm(0.5), "white"], [norm(1.0), "#f6f6f6"]]
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
        plotlim = plt.xlim() + plt.ylim()
        ax.imshow(
            [[1, 0, 1], [1, 0, 1]],
            cmap=cmap,
            interpolation="bicubic",
            extent=plotlim,
            aspect="auto",
        )
        # And plot as normal:
        generate_wardley_plot(ax, wm)
    elif wm.style in ["handwritten"]:
        matplotlib.rcParams["font.family"] = "Gloria Hallelujah"
        fig, ax = plt.subplots(figsize=figsize)
        generate_wardley_plot(ax, wm)
    elif wm.style in ["default", "plain"]:
        fig, ax = plt.subplots(figsize=figsize)
        generate_wardley_plot(ax, wm)
    elif wm.style in plt.style.available:
        with plt.style.context(wm.style):
            fig, ax = plt.subplots(figsize=figsize)
            generate_wardley_plot(ax, wm)
    elif wm.style is not None:
        wm.warnings.append("Map style '%s' not recognised or supported." % wm.style)

    wm.warnings = list(set(wm.warnings))

    return wm, fig


# Actually plot:
def generate_wardley_plot(ax, wm):
    """
    Generates the visual representation of the Wardley Map on the given matplotlib axes.

    Args:
        ax (matplotlib.axes.Axes): The matplotlib axes to draw the map on.
        wm (WardleyMap): The WardleyMap object containing the map data.
    """

    # Set up basic properties:
    if wm.title:
        plt.title(wm.title)
    plt.xlim(0, 1)
    plt.ylim(0, 1.1)

    # Plot the lines
    l = []
    for edge in wm.edges:
        if edge[0] in wm.nodes and edge[1] in wm.nodes:
            n_from = wm.nodes[edge[0]]
            n_to = wm.nodes[edge[1]]
            l.append([(n_from["mat"], n_from["vis"]), (n_to["mat"], n_to["vis"])])
        else:
            for n in edge:
                if n not in wm.nodes:
                    wm.warnings.append(f"Could not find component called {n}!")
    if len(l) > 0:
        lc = LineCollection(l, color=matplotlib.rcParams["axes.edgecolor"], lw=0.5)
        ax.add_collection(lc)

    # Plot blue lines
    b = []
    for blueline in wm.bluelines:
        if blueline[0] in wm.nodes and blueline[1] in wm.nodes:
            n_from = wm.nodes[blueline[0]]
            n_to = wm.nodes[blueline[1]]
            b.append([(n_from["mat"], n_from["vis"]), (n_to["mat"], n_to["vis"])])
        else:
            for n in blueline:
                if n not in wm.nodes:
                    wm.warnings.append(f"Could not find blueline component called {n}!")
    if len(b) > 0:
        lc = LineCollection(b, color="blue", lw=1)
        ax.add_collection(lc)

    # Plot Evolve
    e = []
    for evolve_title, evolve in wm.evolves.items():
        if evolve_title in wm.nodes:
            n_from = wm.nodes[evolve_title]
            e.append([(n_from["mat"], n_from["vis"]), (evolve["mat"], n_from["vis"])])
        else:
            wm.warnings.append(
                f"Could not find evolve component called {evolve_title}!"
            )
    if len(e) > 0:
        lc = LineCollection(e, color="red", lw=0.5, linestyles="dotted")
        ax.add_collection(lc)

    # Add the nodes:
    for node_title in wm.nodes:
        n = wm.nodes[node_title]
        if n["type"] == "component":
            plt.plot(
                n["mat"],
                n["vis"],
                marker="o",
                color=matplotlib.rcParams["axes.facecolor"],
                markeredgecolor=matplotlib.rcParams["axes.edgecolor"],
                markersize=8,
                lw=1,
            )
            ax.annotate(
                node_title,
                fontsize=matplotlib.rcParams["font.size"],
                fontfamily=matplotlib.rcParams["font.family"],
                xy=(n["mat"], n["vis"]),
                xycoords="data",
                xytext=(n["label_x"], n["label_y"]),
                textcoords="offset pixels",
                horizontalalignment="left",
                verticalalignment="bottom",
            )

    # Add the anchors:
    for node_title in wm.nodes:
        n = wm.nodes[node_title]
        if n["type"] == "anchor":
            plt.plot(
                n["mat"],
                n["vis"],
                marker="o",
                color=matplotlib.rcParams["axes.facecolor"],
                markeredgecolor="blue",
                markersize=8,
                lw=1,
            )
            ax.annotate(
                node_title,
                fontsize=matplotlib.rcParams["font.size"],
                fontfamily=matplotlib.rcParams["font.family"],
                xy=(n["mat"], n["vis"]),
                xycoords="data",
                xytext=(n["label_x"], n["label_y"]),
                textcoords="offset pixels",
                horizontalalignment="left",
                verticalalignment="bottom",
            )

    # Add the evolve nodes:
    for evolve_title, evolve in wm.evolves.items():
        if evolve_title in wm.nodes:
            n = wm.nodes[evolve_title]
            plt.plot(
                evolve["mat"],
                n["vis"],
                marker="o",
                color=matplotlib.rcParams["axes.facecolor"],
                markeredgecolor="red",
                markersize=8,
                lw=1,
            )
            ax.annotate(
                evolve_title,
                fontsize=matplotlib.rcParams["font.size"],
                fontfamily=matplotlib.rcParams["font.family"],
                xy=(evolve["mat"], n["vis"]),
                xycoords="data",
                xytext=(n["label_x"], n["label_y"]),
                textcoords="offset pixels",
                horizontalalignment="left",
                verticalalignment="bottom",
            )
        else:
            wm.warnings.append(f"Node '{evolve_title}' does not exist in the map.")

    # Add the pipeline nodes:
    for pipeline_title, pipeline in wm.pipelines.items():
        if pipeline_title in wm.nodes:
            n = wm.nodes[pipeline_title]
            plt.plot(
                n["mat"],
                n["vis"],
                marker="s",
                color=matplotlib.rcParams["axes.facecolor"],
                markersize=8,
                lw=0.5,
            )
        else:
            wm.warnings.append(f"Node '{pipeline_title}' does not exist in the map.")

    # Plot Pipelines
    for pipeline_title, pipeline in wm.pipelines.items():
        if pipeline_title in wm.nodes:
            n_from = wm.nodes[pipeline_title]
            rectangle = patches.Rectangle(
                (pipeline["start_mat"], n_from["vis"] - 0.02),
                pipeline["end_mat"] - pipeline["start_mat"],
                0.02,
                fill=False,
                lw=0.5,
            )
            ax.add_patch(rectangle)
        else:
            wm.warnings.append(
                f"Could not find pipeline component called {pipeline_title}!"
            )

    # Add the notes:
    for note in wm.notes:
        plt.text(
            note["mat"],
            note["vis"],
            note["text"],
            fontsize=matplotlib.rcParams["font.size"],
            fontfamily=matplotlib.rcParams["font.family"],
        )

    plt.yticks(
        [0.0, 0.925], ["Invisible", "Visible"], rotation=90, verticalalignment="bottom"
    )
    plt.ylabel("Visibility", fontweight="bold")
    plt.xticks(
        [0.0, 0.17, 0.4, 0.70],
        ["Genesis", "Custom-Built", "Product\n(+rental)", "Commodity\n(+utility)"],
        ha="left",
    )
    plt.xlabel("Evolution", fontweight="bold")

    plt.tick_params(axis="x", direction="in", top=True, bottom=True, grid_linewidth=1)
    plt.grid(visible=True, axis="x", linestyle="--")
    plt.tick_params(axis="y", length=0)


# Create a SVG of the map plot
def create_svg_map(fig):
    """
    Converts the given matplotlib figure to an SVG string.

    Args:
        map_figure (matplotlib.figure.Figure): The matplotlib figure to convert to SVG.

    Returns:
        str: The SVG representation of the figure.
    """
    # Create a BytesIO object to hold the SVG data
    imgdata = BytesIO()

    # Save the figure to the BytesIO object as SVG
    fig.tight_layout()
    fig.savefig(imgdata, format="svg", bbox_inches='tight')

    # Go to the beginning of the BytesIO object
    imgdata.seek(0)

    # Retrieve the SVG data
    svg_data = imgdata.getvalue()

    # Decode the binary data to string and return
    return svg_data.decode('utf-8')


# Get a Wardley Map from onlinewardleymaps.com
def get_owm_map(map_id):
    url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"

    try:
        response = requests.get(url)

        # Check if the response status code is 200 (successful)
        if response.status_code == 200:
            map_data = response.json()

            # Check if the expected data is present in the response JSON
            if "text" in map_data:
                map_text = map_data["text"]
            else:
                print("Warning: The response JSON does not contain the expected 'text' key.")
                return []
        else:
            print(f"Error: The API request failed with status code {response.status_code}.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error: An error occurred while making the API request: {e}")
        return []

    return map_text
