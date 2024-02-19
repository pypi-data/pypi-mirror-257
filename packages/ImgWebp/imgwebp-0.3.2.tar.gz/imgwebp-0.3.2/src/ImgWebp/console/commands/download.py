from __future__ import annotations

import os

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from ImgWebp.console.command_ui import MyWindow
from ImgWebp.utils.CustomPath import CustomPath
from ImgWebp.utils.download_libwebp import DownloadLibWebP
from ImgWebp.console.commands.command import Command
from ImgWebp.utils.log import log


class DownloadCommandWindow(MyWindow):
    def __init__(self, command):
        super().__init__(command)
        self.is_libwebp = False
        self.customPath = CustomPath(Path(__file__).parent.parent.parent)

    def set_ui(self):
        self.widget = QWidget()
        self.widget.resize(300,200)
        self.widget.setWindowTitle(f"{self.command}操作界面")

        dl = DownloadLibWebP(self.customPath.get_download_dir(), self.customPath.get_lib_dir())
        if os.path.exists(dl.unpack_path):
            self.is_libwebp = True

        bt = QPushButton("开始下载")
        bt.resize(100,50)
        bt.move(90,50)


        msg = QLabel(self.widget)
        msg.resize(100,40)
        msg.move(110,120)

        def set_msg_info(msg_value, msg_type):
            if msg:
                msg.setText(msg_value)
                palette = QPalette()
                palette.setColor(palette.WindowText, msg_type)
                msg.setPalette(palette)
            else:
                msg.setText("")

        if self.is_libwebp:
            bt.setEnabled(not self.is_libwebp)
            set_msg_info("已下载安装",Qt.GlobalColor.green)
            log.info("已下载安装")

        def set_msg(value):
            if value == 200:
                bt.setEnabled(False)
                set_msg_info("下载并安装成功",Qt.GlobalColor.green)
                log.info("下载并安装成功")

        self.dl = DownloadLibWebP(self.customPath.get_download_dir(), self.customPath.get_lib_dir())
        self.dl.download_widget.download_thread.progressChanged.connect(set_msg)
        bt.clicked.connect(self.dl.start)
        bt.setParent(self.widget)
        self.widget.show()




class DownloadCommand(Command):
    name = "download"
    description = (
        "Download the libwebp package."
    )

    def handle(self):
        DownloadCommandWindow(self.name).command_ui()

