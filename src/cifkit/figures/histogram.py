"""Histgoram for supercell size, minimum distances."""

import os

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from cifkit.utils import folder, prompt


def plot_histogram(attribute, stats, dir_path, display, output_dir):
    if not output_dir:
        output_dir = folder.make_output_folder(dir_path, "histograms")

    if attribute == "structure":
        histogram = {
            "data": stats,
            "settings": {
                "file_name": "structures.png",
                "title": "Structures Distribution",
                "xlabel": "Structure",
                "key_data_type": "string",
            },
        }

    if attribute == "formula":
        histogram = {
            "data": stats,
            "settings": {
                "file_name": "formula.png",
                "title": "Formulas Distribution",
                "xlabel": "Formula",
                "key_data_type": "string",
            },
        }

    if attribute == "tag":
        histogram = {
            "data": stats,
            "settings": {
                "file_name": "tag.png",
                "title": "Tags Distribution",
                "xlabel": "Tag",
                "key_data_type": "string",
            },
        }

    if attribute == "space_group_number":
        histogram = {
            "data": stats,
            "settings": {
                "file_name": "space_group_number.png",
                "title": "Space Group Numbers Distribution",
                "xlabel": "Space Group Number",
                "key_data_type": "int",
            },
        }

    if attribute == "space_group_name":
        histogram = {
            "data": stats,
            "settings": {
                "file_name": "space_group_name.png",
                "title": "Space Group Names Distribution",
                "xlabel": "Space Group Name",
                "key_data_type": "string",
            },
        }

    if attribute == "supercell_size":
        histogram = {
            "data": stats,
            "settings": {
                "file_name": "supercell_size.png",
                "title": "Supercell Sizes Distribution",
                "xlabel": "Supercell Size",
                "key_data_type": "int",
            },
        }

    if attribute == "elements":
        histogram = {
            "data": stats,
            "settings": {
                "file_name": "elements.png",
                "title": "Unique Elements Distribution",
                "xlabel": "Element",
                "key_data_type": "string",
            },
        }
    if attribute == "CN_by_min_dist_method":
        histogram = {
            "data": stats,
            "settings": {
                "file_name": "CN_by_min_dist_method.png",
                "title": "Coordination Numbers Distribution by Min Dist Method",
                "xlabel": "Coordination Number",
                "key_data_type": "int",
            },
        }

    if attribute == "CN_by_best_methods":
        histogram = {
            "data": stats,
            "settings": {
                "file_name": "CN_by_best_methods.png",
                "title": "Coordination Numbers Distribution by Best Methods",
                "xlabel": "Coordination Number",
                "key_data_type": "int",
            },
        }

    if attribute == "composition_type":
        histogram = {
            "data": stats,
            "settings": {
                "file_name": "composition_type.png",
                "title": "Unique Composition Types Distribution",
                "xlabel": "Compositions (1: unary, 2: binary, 3: ternary, etc.)",
                "key_data_type": "string",
            },
        }

    if attribute == "site_mixing_type":
        histogram = {
            "data": stats,
            "settings": {
                "file_name": "site_mixing_type.png",
                "title": "Site Mixing Distribution",
                "xlabel": "Site Mixing Type",
                "key_data_type": "string",
            },
        }
    generate_histogram(histogram["data"], histogram["settings"], display, output_dir)

    # Make a default folder if the output folder is not provided


def generate_histogram(data, settings, display, output_dir: str) -> None:
    """Generate a histogram from a dictionary of data and save it to a
    specified directory."""

    plt.figure(figsize=(10, 6))  # Create a new figure for each histogram

    if settings.get("key_data_type") == "float":
        # If keys are supposed to be numeric but are strings, convert them
        data = {float(key): data[key] for key in sorted(data.keys(), key=float)}
    if settings.get("key_data_type") == "int":
        data = {int(key): data[key] for key in sorted(data.keys(), key=int)}

    keys = list(data.keys())
    values = [data[key] for key in keys]

    plt.bar(
        keys,
        values,
        color=settings.get("color", "blue"),
        edgecolor=settings.get("edgecolor", "black"),
    )
    # Custom settings for specific histograms
    file_name = settings.get("file_name")
    if (
        file_name == "CN_by_min_dist_method.png"
        or file_name == "CN_by_best_methods.png"
        or file_name == "composition_type.png"
    ):
        # Assuming keys can be cast to integers, sort and find the range for x-ticks
        int_keys = sorted(map(int, keys))
        plt.xticks(
            range(min(int_keys), max(int_keys) + 1)
        )  # Setting x-ticks to every integer within the range
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    else:
        plt.xticks(rotation=settings.get("rotation", 45), ha="right")

    # y-axis settings
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.ylabel("Count")
    plt.xlabel(settings["xlabel"])

    plt.title(settings["title"])
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.tight_layout()

    output_file_path = folder.get_file_path(output_dir, file_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(output_file_path, dpi=300)
    if display:
        plt.show()  # Display the plot if requested
        plt.close()  # Close the plot after saving and optionally displaying

    prompt.log_save_file_message("Histograms", output_file_path)
