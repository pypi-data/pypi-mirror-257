# WardleyMap

`WardleyMap` is a Python package designed for creating and visualizing Wardley Maps. Wardley Maps provide a visual representation of the strategic landscape and the positioning of components within it, facilitating better decision-making in business strategy and technology development.

## Features

- Parse and interpret Wardley Map syntax.
- Visualize maps using `matplotlib` for easy integration into Python workflows.
- Export maps to SVG format for embedding in web applications or documents.
- With a set of utilities to convert Wardley Map text into JSON, TOML, GRAPH and Cypher Text.

## Installation

Install `wardleymap` using pip:

```bash
pip install wardleymap
```

Ensure you have Python 3.6 or newer installed.

## Quick Start

To create and visualize a Wardley Map, follow these steps:

```python
from wardleymap import wardlemap

# Define the structure of your Wardley Map using a string.
map_definition = """
title Business Value Chain
anchor Customer [0.95, 0.9]
component User Needs [0.8, 0.8]
component Website [0.6, 0.6]
component Hosting [0.3, 0.4]
User Needs -> Website
Website -> Hosting
"""

# Process the Wardley Map text and generate a plot of the map
map, map_plot = wardley(map=map_text)

# Convert the map plot into an SVG
svg_map = create_svg_map(map_plot)
```

## Documentation

For detailed usage and API documentation, please refer to the `docs` directory.

## Contributing

Contributions to `WardleyMap` are welcome! Please read the `CONTRIBUTING.md` file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgements

- Special thanks to the open-source community for the invaluable tools and libraries.
- Inspired by Simon Wardley's work on mapping and strategy.

## Example Usage

Below is an example of how to use the `wardleymap` package to create and visualize a Wardley Map:

```python
from wardleymap import wardlemap

# Define the structure of your Wardley Map using a string.
map_definition = """
title Business Value Chain
anchor Customer [0.95, 0.9]
component User Needs [0.8, 0.8]
component Website [0.6, 0.6]
component Hosting [0.3, 0.4]
User Needs -> Website
Website -> Hosting
"""

# Process the Wardley Map text and generate a plot of the map
map, map_plot = wardley(map=map_text)

# Convert the map plot into an SVG
svg_map = create_svg_map(map_plot)
```
