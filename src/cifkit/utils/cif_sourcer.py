import os


def get_cif_db_source(file_path):
    database_identifiers = {
        "COD": "This file is available in the Crystallography Open Database (COD)",
        "ICSD": "_database_code_ICSD",
        "MS": "'Materials Studio'",
        "PCD": "#_database_code_PCD",
        "MP": "# generated using pymatgen",
        "CCDC": "# Cambridge Structural Database (CSD)",
    }

    if os.path.exists(file_path) and file_path.endswith(".cif"):
        with open(file_path, "r") as file:
            file_content = file.readlines()
            for line in file_content:
                for db_key, db_search_string in database_identifiers.items():
                    if db_search_string in line:
                        return db_key
            return "Unknown"  # Return "Unknown" if no identifier matched
    else:
        return "File does not exist or is not a CIF file"
