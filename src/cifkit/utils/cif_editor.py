from cifkit.utils import cif_parser


def remove_author_loop(file_path: str) -> None:
    """
    Remove the author section from a .cif file to prevent parsing problems
    caused by a wrongly formatted author block.
    """
    (
        start_index,
        end_index,
    ) = cif_parser.get_start_end_line_indexes(
        file_path, "_publ_author_address"
    )

    with open(file_path, "r") as f:
        original_lines = f.readlines()

        # Replace the specific section in original_lines with modified_lines
        original_lines[start_index:end_index] = ["''\n", ";\n", ";\n"]

    with open(file_path, "w") as f:
        f.writelines(original_lines)


# Modify ICSD.cif so that it can be read


def extract_top_header_info(file_path: str) -> None:
    """
    Extract specific information from a .cif file,
    remove surrounding single quotes from the values,
    and print them.
    """

    keys_of_interest = {
        "_chemical_name_common": None,
        "_chemical_formula_structural": None,
        "_chemical_formula_sum": None,
        "_chemical_name_structure_type": None,
        "_exptl_crystal_density_diffrn": None,
    }

    # Read each line of the file and extract the information.
    with open(file_path, "r") as file:
        for line in file:
            # Split the line at the first space to separate key and value.
            if " " in line:
                key, value = line.split(" ", 1)
                # Check if the key is one of interest.
                if key in keys_of_interest:
                    # Remove  whitespace and single quotes from value.
                    value = value.strip().strip("'")
                    # Store the cleaned value.
                    keys_of_interest[key] = value

                    # Check if all keys have been found.
                    if all(
                        value is not None
                        for value in keys_of_interest.values()
                    ):
                        break
    return keys_of_interest


def truncate_content_after_loop(
    file_path: str, output_path: str = None
) -> str:
    """
    Remove the content of a .cif file up to and including the
    first occurrence of 'loop_' nd either save or return
    the remaining content.
    """
    with open(file_path, "r") as file:
        content = file.read()

    # Find the position of the first 'loop_'
    # and keep the content from this point onwards
    loop_index = content.find("loop_")
    if loop_index != -1:
        remaining_content = content[
            loop_index:
        ]  # Include 'loop_' in the remaining content

    if output_path:
        # Save the remaining content to a new file
        # if an output path is provided
        with open(output_path, "w") as output_file:
            output_file.write(remaining_content)

    else:
        # Otherwise, return the remaining content
        return remaining_content


def insert_ICSD_top_header(
    original_file_path: str, data: dict, output_path: str
):
    """
    Inserts extracted key-value data into the
    top section of a .cif file and saves it.
    """

    # Prepare the data to be inserted as formatted strings
    new_content = [
        "data_10-ICSD\n",
        "_audit_creation_date                     2000-00-00\n",
        "_audit_creation_method                   ICSD\n",
    ]

    # Add the extracted data
    for key, value in data.items():
        new_content.append(f"{key} '{value}'\n")

    # Read the original content of the file
    with open(original_file_path, "r") as file:
        original_content = file.readlines()

    # Combine the new data with the original content
    combined_content = new_content + original_content

    # Write the modified content to a new file
    with open(output_path, "w") as output_file:
        output_file.writelines(combined_content)

    print(f"Updated file saved to {output_path}")
