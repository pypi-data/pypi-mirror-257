import os
import wget
import shutil
import platform


class DownloadLibWebP:
    def __init__(self, download_dir, lib_dir):
        self.download_dir = download_dir
        self.lib_dir = lib_dir
        self.libwebp_version = "1.3.2"
        self.unpack_path = self.get_unpack_path()

    def set_libwebp_version(self, version):
        self.libwebp_version = version

    def get_windows_lib(self):
        windows_url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-windows-x64.zip"
        download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-windows-x64.zip")
        self.lib_downloaded(windows_url, download_path)
        self.unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-windows-x64")
        self.lib_unpacked(download_path)

    def get_linux_aarch64_lib(self):
        linux_aarch64_url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-linux-aarch64.tar.gz"
        download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-linux-aarch64.tar.gz")
        self.lib_downloaded(linux_aarch64_url, download_path)

        self.unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-linux-aarch64")
        self.lib_unpacked(download_path)

    def get_linux_x8664_lib(self):
        linux_x8664_url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-linux-x86-64.tar.gz"
        download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-linux-x86-64.tar.gz")
        self.lib_downloaded(linux_x8664_url, download_path)

        self.unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-linux-x86-64")
        self.lib_unpacked(download_path)

    def get_mac_arm64_lib(self):
        mac_arm64_url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-mac-arm64.tar.gz"
        download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-mac-arm64.tar.gz")
        self.lib_downloaded(mac_arm64_url, download_path)

        self.unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-mac-arm64")
        self.lib_unpacked(download_path)

    def get_mac_x8664_lib(self):
        mac_x8664_url = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{self.libwebp_version}-mac-x86-64.tar.gz"
        download_path = os.path.join(self.download_dir, f"libwebp-{self.libwebp_version}-mac-x86-64.tar.gz")
        self.lib_downloaded(mac_x8664_url, download_path)

        self.unpack_path = os.path.join(self.lib_dir, f"libwebp-{self.libwebp_version}-mac-x86-64")
        self.lib_unpacked(download_path)

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

    @staticmethod
    def lib_downloaded(url, download_path):
        if not os.path.exists(download_path):
            wget.download(url, download_path)

    def lib_unpacked(self, download_path):
        format_type = "zip" if platform.system() == "Windows" else "tar"
        if not os.path.exists(self.unpack_path):
            shutil.unpack_archive(download_path, self.lib_dir, format_type)


if __name__ == "__main__":
    from pathlib import Path
    from CustomPath import CustomPath
    customPath = CustomPath(Path(__file__).parent.parent)
    print(customPath.get_package_dir())
