import os
from enum import Enum


class Example(str, Enum):
    # Define 'get_path' as a static method
    @staticmethod
    def get_path(*args):
        # Use '__file__' to get the directory of the current file and join paths
        return os.path.join(os.path.dirname(__file__), *args)

    # Now use 'get_path' to define paths relative to this file
    demo_cif_folder_path = get_path("cifs")
    GdSb_file_path = get_path("cifs", "GdSb.cif")
