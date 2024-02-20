import matplotlib
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re, requests
from io import BytesIO


class WardleyMap:
	"""
	Represents a Wardley Map, allowing for the creation, manipulation, and visualization of strategic business maps.

	Attributes:
		title (str): The title of the map.
		nodes (dict): A dictionary of nodes (components, anchors) in the map, keyed by node title.
		edges (list): A list of tuples representing the connections between nodes.
		bluelines (list): A list of tuples representing special 'blue line' connections between nodes.
		evolutions (dict): A dictionary tracking the evolution status of components.
		evolves (dict): A dictionary of components that are evolving.
		pipelines (dict): A dictionary of pipeline components.
		annotations (list): A list of annotations to be added to the map.
		notes (list): A list of textual notes associated with the map.
		style (str): The visual style of the map.
		warnings (list): A list of warnings generated during map processing.

	Methods:
		__init__(owm): Initializes a WardleyMap object with the given OWM (Own Wardley Markup) syntax.
	"""

	# Developed using https://regex101.com/
	_coords_regexs = "\[\s*([\d\.-]+)\s*,\s*([\d\.-]+)\s*\]"

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

	def __init__(self, owm):
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

		# And load:
		for cl in owm.splitlines():
			cl = cl.strip()
			if not cl:
				continue

			elif cl.startswith("#"):
				# Skip comments...
				continue

			elif cl.startswith("//"):
				# Skip comments...
				continue

			elif cl.startswith("annotation "):
				warning_message = "Displaying annotation not supported yet"
				if warning_message not in self.warnings:
					self.warnings.append(warning_message)
				continue

			elif cl.startswith("annotations "):
				warning_message = "Displaying annotations not supported yet"
				if warning_message not in self.warnings:
					self.warnings.append(warning_message)
				continue

			elif cl.startswith("market "):
				warning_message = "Displaying market not supported yet"
				if warning_message not in self.warnings:
					self.warnings.append(warning_message)
				continue

			elif cl.startswith("pipeline "):
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
				else:
					self.warnings.append("Could not parse pipeline: %s" % cl)

			elif cl.startswith("evolution "):
				warning_message = "Displaying evolution not supported yet"
				if warning_message not in self.warnings:
					self.warnings.append(warning_message)
					continue

			elif cl.startswith("title "):
				self.title = cl.split(" ", maxsplit=1)[1]
				continue

			elif cl.startswith("style "):
				self.style = cl.split(" ", maxsplit=1)[1]
				continue

			elif cl.startswith('anchor '):
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
					self.warnings.append("Could not parse component line: %s" % cl)

			elif cl.startswith('component '):
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
					self.warnings.append("Could not parse component line: %s" % cl)

			elif cl.startswith("evolve "):
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
				else:
					self.warnings.append("Could not parse evolve line: %s" % cl)

			elif "->" in cl:
				edge_parts = cl.split("->")
				if len(edge_parts) != 2:
					self.warnings.append(
						f"Unexpected format for edge definition: {cl}. Skipping this edge."
					)
					continue
				n_from, n_to = edge_parts
				self.edges.append([n_from.strip(), n_to.strip()])

			elif "+<>" in cl:
				edge_parts = cl.split("+<>")
				if len(edge_parts) != 2:
					self.warnings.append(
						f"Unexpected format for blueline definition: {cl}. Skipping this edge."
					)
					continue
				n_from, n_to = edge_parts
				self.bluelines.append([n_from.strip(), n_to.strip()])
				continue

			elif cl.startswith("note"):
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
				else:
					self.warnings.append("Could not parse note line: %s" % cl)
			else:
				# Warn about lines we can't handle?
				self.warnings.append("Could not parse line: %s" % cl)

		self.warnings = list(set(self.warnings))


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
