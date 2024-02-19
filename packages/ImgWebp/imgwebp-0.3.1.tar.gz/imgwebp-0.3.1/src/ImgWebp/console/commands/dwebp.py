from __future__ import annotations

from PyQt5.QtWidgets import QFileDialog, QLineEdit, QPushButton, QRadioButton, QLabel, QButtonGroup
from ImgWebp.console.command_ui import CommandWindow
from ImgWebp.utils.script import CommandParameter
from ImgWebp.console.commands.command import Command
from ImgWebp.utils.log import log


class DwebpCommandWindow(CommandWindow):
    def __init__(self, command):
        super().__init__(command)
        self.output_type = None

    def set_input_btn(self):
        inputBtn = QPushButton("输入文件或文件夹", self.commandUi)
        inputBtn.resize(150, 30)
        inputBtn.move(400, 35)
        inputBtn.clicked.connect(lambda: self.openDialog(QFileDialog.AnyFile))

        self.inputLine = QLineEdit(self.commandUi)
        self.inputLine.resize(350, 28)
        self.inputLine.move(30, 35)

    def set_output_btn(self):
        outputBtn = QPushButton("输出文件夹", self.commandUi)
        outputBtn.resize(150, 30)
        outputBtn.move(400, 120)
        outputBtn.clicked.connect(lambda: self.openDialog(QFileDialog.DirectoryOnly))

        self.outputLine = QLineEdit(self.commandUi)
        self.outputLine.resize(350, 28)
        self.outputLine.move(30, 120)

        bg = QButtonGroup(self.commandUi)

        label = QLabel("输出格式：", self.commandUi)
        label.move(30, 90)
        pngBtn = QRadioButton("PNG", self.commandUi)
        pngBtn.move(90, 90)
        pamBtn = QRadioButton("PAM", self.commandUi)
        pamBtn.move(150, 90)
        ppmBtn = QRadioButton("PPM", self.commandUi)
        ppmBtn.move(210, 90)
        pgmBtn = QRadioButton("PGM", self.commandUi)
        pgmBtn.move(270, 90)

        bg.addButton(pngBtn, 1)
        bg.addButton(pamBtn, 2)
        bg.addButton(ppmBtn, 3)
        bg.addButton(pgmBtn, 4)

        bg.buttonClicked.connect(self.set_output_type)

    def set_output_type(self, button):
        self.output_type = button.text().lower()

    def openDialog(self, mode):
        fileDialog = QFileDialog(self.commandUi)
        fileDialog.setWindowTitle("标题")
        fileDialog.setFileMode(mode)
        fileDialog.setDirectory("/")
        fileDialog.setNameFilter("Images (*.webp)")
        # 窗口显示，返回文件路径
        file_path = fileDialog.exec()
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
            self.msg.setText("输入文件或文件夹不能为空")
            return False

        if not self.output_type:
            self.msg.setText("请选择输出格式")
            return False

        self.command_parameter = CommandParameter(self.command, input_path, output_path).set_output_type(
            self.output_type)
        return True


class DwebpCommand(Command):
    name = "dwebp"
    description = (
        "decompress a WebP file to an image file."
    )

    def handle(self):
        DwebpCommandWindow(self.name).command_ui()
