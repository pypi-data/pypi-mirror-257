import os.path
import shutil

from ImgWebp.utils.download_libwebp import DownloadLibWebP
from ImgWebp.utils.CustomPath import CustomPath
from pathlib import Path

def get_unpack_path():
    customPath = CustomPath(Path(__file__).parent.parent)
    dl = DownloadLibWebP(customPath.get_download_dir(),customPath.get_lib_dir(),False)
    return dl.unpack_path

def get_tmp_path():
    customPath = CustomPath(Path(__file__).parent.parent)
    return customPath.get_custom_dir("tmp")

def remove_tmp():
    tmp_path = get_tmp_path()
    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)
