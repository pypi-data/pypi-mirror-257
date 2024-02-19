from __future__ import annotations

from PyQt5.QtWidgets import QFileDialog, QLineEdit, QPushButton
from ImgWebp.console.command_ui import CommandWindow
from ImgWebp.utils.script import CommandParameter
from ImgWebp.console.commands.command import Command
from ImgWebp.utils.log import log


class CwebpCommandWindow(CommandWindow):
    def __init__(self, command):
        super().__init__(command)

    def set_input_btn(self):
        inputBtn = QPushButton("输入文件或文件夹", self.commandUi)
        inputBtn.resize(150, 30)
        inputBtn.move(400, 50)
        inputBtn.clicked.connect(lambda: self.openDialog(QFileDialog.AnyFile))

        self.inputLine = QLineEdit(self.commandUi)
        self.inputLine.resize(350, 28)
        self.inputLine.move(30, 50)

    def set_output_btn(self):
        outputBtn = QPushButton("输出文件夹", self.commandUi)
        outputBtn.resize(150, 30)
        outputBtn.move(400, 120)
        outputBtn.clicked.connect(lambda: self.openDialog(QFileDialog.DirectoryOnly))

        self.outputLine = QLineEdit(self.commandUi)
        self.outputLine.resize(350, 28)
        self.outputLine.move(30, 120)

    def openDialog(self, mode):
        fileDialog = QFileDialog(self.commandUi)
        fileDialog.setWindowTitle("标题")
        fileDialog.setFileMode(mode)
        fileDialog.setDirectory("/")
        fileDialog.setNameFilter("Images (*.png *.jpeg *.jpg *.tiff)")
        file_path = fileDialog.exec()  # 窗口显示，返回文件路径
        if file_path and fileDialog.selectedFiles():
            if mode == QFileDialog.DirectoryOnly:
                self.outputLine.setText(fileDialog.selectedFiles()[0])
                log.info("{} 输出路径为：{}".format(self.command, fileDialog.selectedFiles()[0]))
            else:
                self.inputLine.setText(fileDialog.selectedFiles()[0])
                log.info("{} 输入路径为：{}".format(self.command, fileDialog.selectedFiles()[0]))

    def check(self):
        input_path = self.inputLine.text()
        output_path = self.outputLine.text()
        if input_path == "" or output_path == "":
            msg = "输入文件或文件夹不能为空"
            self.msg.setText(msg)
            return False

        self.command_parameter = CommandParameter(self.command, input_path, output_path)
        return True

class CwebpCommand(Command):
    name = "cwebp"
    description = (
        "compress an image file to a WebP file."
    )

    def handle(self):
        CwebpCommandWindow(self.name).command_ui()
