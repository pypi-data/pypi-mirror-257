import os
import wget
import shutil
import platform

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QProgressBar, QHBoxLayout
from PyQt5.QtGui import QFont


class DownloadLibWebP:
    def __init__(self, download_dir, lib_dir):
        self.download_dir = download_dir
        self.lib_dir = lib_dir
        self.libwebp_version = "1.3.2"
        self.unpack_path = self.get_unpack_path()
        self.download_libwebp()

    def set_libwebp_version(self, version):
        self.libwebp_version = version

    def get_windows_lib(self):
        self.url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-windows-x64.zip"
        self.download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-windows-x64.zip")
        self.unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-windows-x64")

    def get_linux_aarch64_lib(self):
        self.url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-linux-aarch64.tar.gz"
        self.download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-linux-aarch64.tar.gz")
        self.unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-linux-aarch64")

    def get_linux_x8664_lib(self):
        self.url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-linux-x86-64.tar.gz"
        self.download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-linux-x86-64.tar.gz")
        self.unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-linux-x86-64")

    def get_mac_arm64_lib(self):
        self.url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-mac-arm64.tar.gz"
        self.download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-mac-arm64.tar.gz")
        self.unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-mac-arm64")

    def get_mac_x8664_lib(self):
        self.url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-mac-x86-64.tar.gz"
        self.download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-mac-x86-64.tar.gz")
        self.unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-mac-x86-64")

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

        return unpack_path

    def lib_unpacked(self):
        format_type = "zip" if platform.system() == "Windows" else "tar"
        if not os.path.exists(self.unpack_path):
            shutil.unpack_archive(self.download_path, self.lib_dir, format_type)

    def start(self):
        import sys
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        download_widget = DownloadWidget(self.url, self.download_path)
        download_widget.show()
        code = app.exec_()
        if code == 0:
            self.lib_unpacked()
        sys.exit(code)


class DownloadWidget(QWidget):
    def __init__(self, url, download_path):
        super().__init__()
        self.setWindowTitle('libwebp下载中...')
        layout = QHBoxLayout(self)

        # 创建进度条
        self.progressBar = QProgressBar(self, minimumWidth=400)
        self.progressBar.setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 5px; background-color: "
                                       "#FFFFFF; text-align: center;}QProgressBar::chunk {background:QLinearGradient("
                                       "x1:0,y1:0,x2:2,y2:0,stop:0 #666699,stop:1  #DB7093); }")

        font = QFont()
        font.setBold(True)
        font.setWeight(30)
        self.progressBar.setFont(font)

        self.progressBar.setValue(0)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setFormat('Loaded  %p%'.format(self.progressBar.value() - self.progressBar.minimum()))

        layout.addWidget(self.progressBar)

        # 创建并启动下载线程
        self.download_thread = DownloadThread(url, download_path)
        self.download_thread.progressChanged.connect(self.update_progress)
        self.download_thread.start()

    # 更新进度条
    def update_progress(self, value):
        if value == 100:
            print('下载完成！！！！！！')
            self.close()
        self.progressBar.setValue(value)


class DownloadThread(QThread):
    # 定义信号
    progressChanged = pyqtSignal(int)

    def __init__(self, url, download_path):
        super().__init__()
        self.url = url
        self.download_path = download_path

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
    from pathlib import Path
    from CustomPath import CustomPath

    customPath = CustomPath(Path(__file__).parent.parent)

    dl = DownloadLibWebP(customPath.get_download_dir(),customPath.get_lib_dir())
    dl.start()
