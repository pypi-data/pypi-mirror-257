"""
Generates a visual representation of a Wardley Map using Matplotlib.

This function takes a Wardley Map object as input and utilizes Matplotlib to generate
a visual representation of the map. It supports various styles for the map, such as 'wardley',
'handwritten', 'default', and 'plain', among others available in Matplotlib. The function
configures the plot's appearance, including font, title, axes, and grid lines. It then adds
the Wardley Map components like nodes, edges, annotations, and special features such as
evolve markers and pipeline representations to the plot. The output is a Matplotlib figure
object, which can be displayed in a Jupyter notebook or saved as an image file.

Parameters:
    map (WardleyMap): An instance of the WardleyMap class containing the elements and
    properties of the map to be visualized, including components, relationships, and annotations.

Returns:
    matplotlib.figure.Figure: A Matplotlib figure object representing the Wardley Map. This object
    can be used to display the map within a Jupyter notebook or saved to a file in formats supported
    by Matplotlib, such as PNG or SVG.

Raises:
    ValueError: If an unrecognized style is specified in the WardleyMap object.
    KeyError: If a node referenced in edges, bluelines, evolves, or pipelines is not defined in the map.

Notes:
    The function automatically adjusts the plot settings based on the specified style in the WardleyMap object.
    It supports advanced customization through the WardleyMap object, allowing users to define specific aspects
        of the map, such as evolution stages, visibility levels, and custom annotations.
    Warnings are generated and appended to the WardleyMap object's warnings attribute for any inconsistencies or
        issues detected during the map generation process, such as missing components or unsupported styles.
"""

import matplotlib
from matplotlib import patches
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from .wardley_maps import WardleyMap


def initialize_plot(figsize=(24, 15)):
    """
    Initializes a Matplotlib figure and axes for plotting a Wardley Map.

    This function sets up a Matplotlib figure with specified dimensions and configures the plot area (axes)
    with predefined limits for the x and y axes suitable for Wardley Maps. The x-axis represents the evolution
    axis, ranging from 0 (Genesis) to 1 (Commodity), and the y-axis represents the visibility axis,
    ranging from 0 (Invisible) to slightly above 1 to provide a margin.

    It also resets Matplotlib's configuration to the default settings to ensure that any previous customizations
    do not affect the appearance of the Wardley Map plot. This is crucial for maintaining consistency in the
    visualization output, especially when the function is used in environments where multiple plots might be
    generated within the same session.

    Parameters:
        wm (WardleyMap): The WardleyMap object for which the plot is being initialized. Currently, this parameter
            is not used within the function but is included for potential future enhancements where plot
            initialization might depend on attributes of the WardleyMap object.
        figsize (tuple): A tuple specifying the width and height of the figure in inches. The default size
            is set to (10, 7) inches, which provides a balanced aspect ratio for typical Wardley Maps.

    Returns:
        fig (matplotlib.figure.Figure): The Matplotlib figure object for the plot. This object provides
            the canvas for the plot and can be used to save the plot to a file or display it in a notebook.
        ax (matplotlib.axes.Axes): The Matplotlib axes object for the plot. This object represents the plot
            area where graphical elements like nodes, edges, and annotations are drawn.

    Example:
        >>> wm = WardleyMap(owm_syntax)
        >>> fig, ax = initialize_plot(wm)
        >>> # Now you can use `ax` to add elements to the plot, and `fig` to save or display the plot.
    """

    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.1)
    return fig, ax


def create_wardley_map_plot(wardley_map):
    """
    Generates a visual representation of a Wardley Map using Matplotlib.

    This function takes a Wardley Map object as input, which contains information about
    components, edges, anchors, pipelines, and notes of the map.
    It supports different styles for the map visualization,
    including 'wardley', 'handwritten', 'default', 'plain',
    and other Matplotlib styles. The function configures various aspects of the plot,
    such as font, title, axes, and grid lines, and adds elements of the Wardley Map,
    such as nodes, edges, and annotations, to the plot.

    Parameters:
        map (WardleyMap): An instance of the WardleyMap class containing
        the elements and properties of the map to be visualized.

    Returns:
        matplotlib.figure.Figure: A Matplotlib figure object representing the Wardley Map.
        This object can be used to display the map within a Jupyter notebook or save it to a file.
    """

    # Parse the OWM syntax:
    wm = WardleyMap(wardley_map)

    # Initialise the plot
    fig, ax = initialize_plot()

    if wm.style is None:
        wm.style = "wardley"

    if wm.style == "wardley":
        # Use a monospaced font:
        matplotlib.rcParams["font.family"] = "monospace"
        matplotlib.rcParams["font.size"] = 6
        # Set up the default plot:
        # fig, ax = plt.subplots(figsize=figsize)
        # fig, ax = plt.subplots()
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
    if wm.style in ["handwritten"]:
        matplotlib.rcParams["font.family"] = "Gloria Hallelujah"
        # fig, ax = plt.subplots(figsize=figsize)
        fig, ax = plt.subplots()
    if wm.style in ["default", "plain"]:
        # fig, ax = plt.subplots(figsize=figsize)
        fig, ax = plt.subplots()
    if wm.style in plt.style.available:
        with plt.style.context(wm.style):
            # fig, ax = plt.subplots(figsize=figsize)
            fig, ax = plt.subplots()
    if wm.style is not None:
        wm.warnings.append(f"Map style '{wm.style}' not recognised or supported.")

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
    for node_title, n in wm.nodes.items():
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
    for node_title, n in wm.nodes.items():
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
    for pipeline_title, _pipeline in wm.pipelines.items():
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

    wm.warnings = list(set(wm.warnings))

    return fig
