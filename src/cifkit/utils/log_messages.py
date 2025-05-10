from enum import Enum


class CifLog(Enum):
    PREPROCESSING = "Preprocessing {file_path}"
    LOADING_DATA = "Parsing .cif and generating supercell for {file_name}"
    COMPUTE_CONNECTIONS = "Computing pair distances for {file_name}"


class CifEnsembleLog(Enum):
    PREPROCESSING = "Preprocessing {dir_path}"
