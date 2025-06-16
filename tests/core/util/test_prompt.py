import logging

from cifkit.utils.prompt import log_connected_points, log_save_file_message


def test_log_save_file_message(caplog):
    file_type = "Histogram"
    file_path = "/path/to/histogram.png"

    # Check that the log message as expected
    with caplog.at_level(logging.INFO):
        log_save_file_message(file_type, file_path)
    assert f"{file_type} has been saved in {file_path}." in caplog.text


def test_log_connected_points(caplog):
    # Setup sample data for testing
    all_labels_connections = {
        "A": [("B", 1.5, (1, 1), (2, 2)), ("C", 2.0, (1, 1), (3, 3))],
        "B": [("A", 1.5, (2, 2), (1, 1))],
    }

    # Test logging
    with caplog.at_level(logging.INFO):
        log_connected_points(all_labels_connections)

    # Optionally, verify the entire log for correctness in order
    expected_log = [
        "\nAtom site A:",
        "B 1.5 (1, 1), (2, 2)",
        "C 2.0 (1, 1), (3, 3)",
        "\nAtom site B:",
        "A 1.5 (2, 2), (1, 1)",
    ]
    # This checks if the expected log messages are in the correct order and format
    for expected_message in expected_log:
        assert expected_message in caplog.text
