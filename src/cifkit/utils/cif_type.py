def get_cif_file_source(file_path):
    """
    Check if the file contains the line '_database_code_ICSD'.
    """
    with open(file_path, "r") as file:
        for line in file:
            if "_database_code_ICSD" in line:
                return "ICSD"
            elif "_database_code_PCD" in line:
                return "PCD"
            elif "_cod_database_code" in line:
                return "COD"
        # If no return statement was hit during the loop, raise an error after the loop
        raise ValueError(
            "The provided CIF file does not contain recognized markers for ICSD, PCD, or COD databases. "
            "Please verify the file and try again."
        )
