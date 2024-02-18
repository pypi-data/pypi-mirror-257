import os
from pathlib import Path


class CustomPath:

    def __init__(self, filename: Path):
        self.filename = filename

    def get_package_dir(self):
        return self.filename

    def get_src_dir(self):
        return self.get_package_dir().parent

    def get_root_dir(self):
        return self.get_src_dir().parent

    def get_data_dir(self):
        data_dir = f"{self.get_root_dir()}/data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        return data_dir

    def get_lib_dir(self):
        lib_dir = f"{self.get_root_dir()}/data/lib"
        if not os.path.exists(lib_dir):
            os.makedirs(lib_dir)
        return lib_dir

    def get_download_dir(self):
        download_dir = f"{self.get_root_dir()}/data/download"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        return download_dir
