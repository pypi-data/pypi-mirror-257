import os
import wget
import shutil
import platform
from ImgWebp.utils.log import logger

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QProgressBar, QHBoxLayout, QPushButton, qApp
from PyQt5.QtGui import QFont


class DownloadLibWebP:
    def __init__(self, download_dir, lib_dir):
        self.download_widget = None
        self.download_path = None
        self.url = None
        self.download_dir = download_dir
        self.lib_dir = lib_dir
        self.libwebp_version = "1.3.2"
        self.download_libwebp()
        self.unpack_path = self.get_unpack_path()
        self.start_before()

    def set_libwebp_version(self, version):
        self.libwebp_version = version

    def get_windows_lib(self):
        self.url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-windows-x64.zip"
        self.download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-windows-x64.zip")
        logger.info(f"获取下载地址：{self.url}")
        logger.info(f"获取下载路径：{self.download_path}")

    def get_linux_aarch64_lib(self):
        self.url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-linux-aarch64.tar.gz"
        self.download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-linux-aarch64.tar.gz")
        logger.info(f"获取下载地址：{self.url}")
        logger.info(f"获取下载路径：{self.download_path}")

    def get_linux_x8664_lib(self):
        self.url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-linux-x86-64.tar.gz"
        self.download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-linux-x86-64.tar.gz")
        logger.info(f"获取下载地址：{self.url}")
        logger.info(f"获取下载路径：{self.download_path}")

    def get_mac_arm64_lib(self):
        self.url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-mac-arm64.tar.gz"
        self.download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-mac-arm64.tar.gz")
        logger.info(f"获取下载地址：{self.url}")
        logger.info(f"获取下载路径：{self.download_path}")

    def get_mac_x8664_lib(self):
        self.url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-mac-x86-64.tar.gz"
        self.download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-mac-x86-64.tar.gz")
        logger.info(f"获取下载地址：{self.url}")
        logger.info(f"获取下载路径：{self.download_path}")

    def download_libwebp(self):
        platform_type = platform.system()
        machine = platform.machine()
        if platform_type == "Linux":
            if machine == "aarch64":
                self.get_linux_aarch64_lib()
            elif machine == "x86_64":
                self.get_linux_x8664_lib()
        elif platform_type == "Darwin":
            if machine == "arm64":
                self.get_mac_arm64_lib()
            elif machine == "x86_64":
                self.get_mac_x8664_lib()
        else:
            if platform.architecture()[0] == "64bit":
                self.get_windows_lib()
            else:
                raise Exception("Unsupported platform")

    def get_unpack_path(self):
        global unpack_path
        platform_type = platform.system()
        machine = platform.machine()
        if platform_type == "Linux":
            if machine == "aarch64":
                unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-linux-aarch64")
            elif machine == "x86_64":
                unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-linux-x86-64")
        elif platform_type == "Darwin":
            if machine == "arm64":
                unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-mac-arm64")
            elif machine == "x86_64":
                unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-mac-x86-64")
        else:
            if platform.architecture()[0] == "64bit":
                unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-windows-x64")
            else:
                raise Exception("Unsupported platform")
        logger.info(f"获取包解压安装路径: {unpack_path}")
        return unpack_path

    def lib_unpacked(self, value):
        if value == 100:
            format_type = "zip" if platform.system() == "Windows" else "tar"
            if not os.path.exists(self.unpack_path):
                shutil.unpack_archive(self.download_path, self.lib_dir, format_type)
                self.download_widget.download_thread.progressChanged.emit(100)

    def start_before(self):
        self.download_widget = DownloadWidget(self.url, self.download_path)
        self.download_widget.download_thread.progressChanged.connect(self.lib_unpacked)

    def start(self):
        self.download_widget.start_download()
        self.download_widget.show()


class DownloadWidget(QWidget):
    def __init__(self, url, download_path):
        super().__init__()
        self.setWindowTitle('libwebp下载中...')
        # 设置UI
        self.set_ui()
        # 创建下载线程
        self.download_thread = DownloadThread(url, download_path)
        self.download_thread.progressChanged.connect(self.update_progress)

    def set_ui(self):
        layout = QHBoxLayout(self)

        # 创建进度条
        self.progressBar = QProgressBar(self, minimumWidth=400)

        with open("Download.qss", "r") as f:
            qApp.setStyleSheet(f.read())

        font = QFont()
        font.setBold(True)
        font.setWeight(30)
        self.progressBar.setFont(font)

        self.progressBar.setValue(0)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setFormat('Loaded  %p%'.format(self.progressBar.value() - self.progressBar.minimum()))

        layout.addWidget(self.progressBar)

    def start_download(self):
        # 启动下载线程
        logger.info('启动下载线程...')
        self.download_thread.start()

    # 更新进度条
    def update_progress(self, value):
        if value == 100:
            logger.info('下载完成...')
            self.close()
        self.progressBar.setValue(value)


class DownloadThread(QThread):
    # 定义信号
    progressChanged = pyqtSignal(int)

    def __init__(self, url, download_path):
        super().__init__()
        self.url = url
        self.download_path = download_path
        logger.info("初始化下载线程...")

    def run(self):
        self.lib_downloaded(self.url, self.download_path)

    def lib_downloaded(self, url, download_path):
        if not os.path.exists(download_path):
            wget.download(url, download_path, self.progress_bar_callback)

        self.progressChanged.emit(100)

    # 回调函数，用于更新进度条
    def progress_bar_callback(self, current, total, width=80):
        progress = current / total * 100
        self.progressChanged.emit(int(progress))


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    from pathlib import Path
    from CustomPath import CustomPath

    def qwe(value):
        print(value)


    customPath = CustomPath(Path(__file__).parent.parent)

    q = QWidget()

    dl = DownloadLibWebP(customPath.get_download_dir(), customPath.get_lib_dir())
    dl.download_widget.download_thread.progressChanged.connect(qwe)
    bt = QPushButton("开始下载")
    bt.clicked.connect(dl.start)
    bt.setParent(q)
    q.show()

    sys.exit(app.exec_())
