import logging


def log_connected_points(all_labels_connections):
    """Print nearest neighbor information."""
    for label, connections in all_labels_connections.items():
        logging.info(f"\nAtom site {label}:")
        for (
            label,
            dist,
            coords_1,
            coords_2,
        ) in connections:
            logging.info(f"{label} {dist} {coords_1}, {coords_2}")


def log_save_file_message(file_type: str, file_path: str):
    """Print when a file is saved."""
    logging.info(f"{file_type} has been saved in {file_path}.")
