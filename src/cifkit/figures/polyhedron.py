import os

import numpy as np
import pyvista as pv
from scipy.spatial import ConvexHull, Delaunay


def generate_contrasting_colors() -> list[str]:
    """Return a list of manually selected contrasting colors."""
    return [
        "#00FFFF",  # Cyan
        "#0000FF",  # Blue
        "#FF0000",  # Red
        "#800080",  # Purple
        "#FF00FF",  # Magenta
        "#FFFF00",  # Yellow
        "#00FF00",  # Lime
        "#FF4500",  # Orange Red
        "#2E8B57",  # Sea Green
        "#1E90FF",  # Dodger Blue
        "#FF1493",  # Deep Pink
        "#FFD700",  # Gold
    ]


def generate_color_mapping(labels):
    """Generate a dictionary mapping labels to contrasting colors."""
    colors = generate_contrasting_colors()
    color_map = {}
    unique_labels = set(labels)
    for i, label in enumerate(unique_labels):
        color_map[label] = colors[i % len(colors)]
    return color_map


def plot(
    points,
    vertex_labels,
    file_path,
    formula,
    show_labels,
    is_displayed,
    output_dir=None,
):
    """Generate and save a 3D plot of a molecular structure."""

    plotter = pv.Plotter(off_screen=not is_displayed, window_size=(1600, 1200))
    label_colors = generate_color_mapping(vertex_labels)

    points = np.array(points)
    central_atom_coord = points[-1]
    central_atom_label = vertex_labels[-1]
    # Coordination numbers
    coordination_number = len(points) - 1

    # Title
    title = (
        f"Formula: {formula}, Central atom: {central_atom_label}, "
        f"CN: {coordination_number},\n{file_path}"
    )

    plotter.add_title(title, font="arial")
    # Constructing title and subtitle

    for idx, (point, label) in enumerate(zip(points, vertex_labels)):
        radius = (
            0.4 if np.array_equal(point, central_atom_coord) else 0.4
        )  # Central atom larger
        sphere = pv.Sphere(radius=radius, center=point)
        plotter.add_mesh(sphere, color=label_colors[label])

        # Creating a label with numbering
        indexed_label = f"{idx + 1}. {label}"
        adjusted_point = point + [
            0.3,
            0.3,
            0.3,
        ]  # Offset to avoid overlapping with the sphere

        if show_labels:
            if idx != len(points) - 1:
                plotter.add_point_labels(
                    adjusted_point,
                    [indexed_label],  # Use the indexed label
                    font_size=50,
                    text_color=label_colors[label],
                    always_visible=True,
                    shape=None,
                    margin=0,
                    reset_camera=False,
                )

    delaunay = Delaunay(points)
    hull = ConvexHull(points, qhull_options="QJ")

    edges = set()
    for simplex in delaunay.simplices:
        for i in range(4):
            for j in range(i + 1, 4):
                edge = tuple(sorted([simplex[i], simplex[j]]))
                edges.add(edge)

    hull_edges = set()
    for simplex in hull.simplices:
        for i in range(len(simplex)):
            for j in range(i + 1, len(simplex)):
                hull_edge = tuple(sorted([simplex[i], simplex[j]]))
                hull_edges.add(hull_edge)

    for edge in edges:
        if edge in hull_edges:
            start, end = points[edge[0]], points[edge[1]]
            cylinder = pv.Cylinder(
                center=(start + end) / 2,
                direction=end - start,
                radius=0.05,
                height=np.linalg.norm(end - start),
            )
            plotter.add_mesh(cylinder, color="grey")

    faces = []
    for simplex in hull.simplices:
        faces.append([3] + list(simplex))
    poly_data = pv.PolyData(points, faces)

    plotter.add_mesh(poly_data, color="aqua", opacity=0.5, show_edges=True)

    plotter.show()
    """Output."""

    # Determine the output directory based on provided path
    if not output_dir:
        output_dir = os.path.join(os.path.dirname(file_path), "polyhedrons")

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Use the filename from file_path and append the central atom label
    plot_filename = (
        os.path.basename(file_path).replace(".cif", "")
        + "_"
        + central_atom_label
        + ".png"
    )
    save_path = os.path.join(output_dir, plot_filename)
    """Save."""
    # Save the screenshot
    plotter.screenshot(save_path)
