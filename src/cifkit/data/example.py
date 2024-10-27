import os
from enum import Enum


class Example(str, Enum):
    # Define 'get_path' as a static method
    @staticmethod
    def get_path(*args):
        # Use '__file__' to get the directory of the current file and join paths
        return os.path.join(os.path.dirname(__file__), *args)

    # Now use 'get_path' to define paths relative to this file
    ErCoIn_folder_path = get_path("ErCoIn")
    ErCoIn_big_folder_path = get_path("ErCoIn_big")
    Er10Co9In20_file_path = get_path("ErCoIn", "Er10Co9In20.cif")
    Er5In3_file_path = get_path("ErCoIn", "Er5In3.cif")
    ErCoIn5_file_path = get_path("ErCoIn", "ErCoIn5.cif")
