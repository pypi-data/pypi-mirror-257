# Create a Wardley Map PNG or SVG
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from WardleyMaps import WardleyMap


def createwardleymap(map):
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
    colors = [[norm(0.0), "white"], [norm(0.5), "white"],
              [norm(1.0), "#f6f6f6"]]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    plotlim = plt.xlim() + plt.ylim()
    ax.imshow([[1, 0, 1], [1, 0, 1]],
              cmap=cmap,
              interpolation="bicubic",
              extent=plotlim,
              aspect="auto")
  elif wm.style in ["handwritten"]:
    matplotlib.rcParams["font.family"] = "Gloria Hallelujah"
    fig, ax = plt.subplots(figsize=figsize)
  elif wm.style in ["default", "plain"]:
    fig, ax = plt.subplots(figsize=figsize)
  elif wm.style in plt.style.available:
    with plt.style.context(wm.style):
      fig, ax = plt.subplots(figsize=figsize)
  elif wm.style is not None:
    wm.warnings.append("Map style '%s' not recognised or supported." %
                       wm.style)

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
      e.append([(n_from["mat"], n_from["vis"]),
                (evolve["mat"], n_from["vis"])])
    else:
      wm.warnings.append(
          f"Could not find evolve component called {evolve_title}!")
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
          f"Could not find pipeline component called {pipeline_title}!")

  # Add the notes:
  for note in wm.notes:
    plt.text(
        note["mat"],
        note["vis"],
        note["text"],
        fontsize=matplotlib.rcParams["font.size"],
        fontfamily=matplotlib.rcParams["font.family"],
    )

  plt.yticks([0.0, 0.925], ["Invisible", "Visible"],
             rotation=90,
             verticalalignment="bottom")
  plt.ylabel("Visibility", fontweight="bold")
  plt.xticks(
      [0.0, 0.17, 0.4, 0.70],
      [
          "Genesis", "Custom-Built", "Product\n(+rental)",
          "Commodity\n(+utility)"
      ],
      ha="left",
  )
  plt.xlabel("Evolution", fontweight="bold")

  plt.tick_params(axis="x",
                  direction="in",
                  top=True,
                  bottom=True,
                  grid_linewidth=1)
  plt.grid(visible=True, axis="x", linestyle="--")
  plt.tick_params(axis="y", length=0)

  wm.warnings = list(set(wm.warnings))

  return fig