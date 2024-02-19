from __future__ import annotations

from PyQt5.QtWidgets import QFileDialog, QLineEdit, QPushButton, QLabel, QSpinBox, QComboBox
from PyQt5.QtCore import Qt
from ImgWebp.console.command_ui import CommandWindow
from ImgWebp.utils.script import CommandParameter
from ImgWebp.console.commands.command import Command
from ImgWebp.utils.log import log


class Img2WebpCommandWindow(CommandWindow):
    def __init__(self, command):
        super().__init__(command)
        self.output_type = None

    def set_input_btn(self):
        self.commandUi.resize(600, 280)

        inputBtn = QPushButton("输入文件或文件夹", self.commandUi)
        inputBtn.resize(150, 30)
        inputBtn.clicked.connect(lambda: self.openDialog(QFileDialog.ExistingFiles))

        self.inputLine = QLineEdit(self.commandUi)
        self.inputLine.resize(350, 28)

        imgSize = QLabel("输入图片大小（大小一致可以不用设置）：", self.commandUi)
        imgSize.resize(250, 30)

        widthLabel = QLabel("宽：", self.commandUi)
        widthLabel.resize(20, 30)

        self.width = QLineEdit(self.commandUi)
        self.width.resize(60, 28)

        heightLabel = QLabel("高：", self.commandUi)
        heightLabel.resize(20, 30)

        self.height = QLineEdit(self.commandUi)
        self.height.resize(60, 28)

        # move
        inputBtn.move(400, 20)
        self.inputLine.move(30, 20)

        imgSize.move(30, 60)
        widthLabel.move(285, 60)
        self.width.move(305, 60)
        heightLabel.move(380, 60)
        self.height.move(400, 60)

    def set_output_btn(self):
        outputBtn = QPushButton("输出文件夹", self.commandUi)
        outputBtn.resize(150, 30)
        outputBtn.clicked.connect(lambda: self.openDialog(QFileDialog.DirectoryOnly))

        self.outputLine = QLineEdit(self.commandUi)
        self.outputLine.resize(350, 28)

        loopLabel = QLabel("动画循环次数（0代表无限循环）：", self.commandUi)
        loopLabel.resize(200, 30)

        self.loop = QSpinBox(self.commandUi)
        self.loop.setRange(0, 1000)
        self.loop.resize(60, 28)

        qualityLabel = QLabel("图片质量：", self.commandUi)
        qualityLabel.resize(80, 30)

        self.quality = QComboBox(self.commandUi)
        self.quality.addItems(["混合", "无损", "有损"])
        self.quality.resize(90, 28)

        timeLabel = QLabel("每张图片时长（毫秒）：", self.commandUi)
        timeLabel.resize(150, 30)

        self.time = QSpinBox(self.commandUi)
        self.time.resize(100, 28)
        self.time.setRange(0, 1000 * 60 * 60 * 24 * 7)

        # move

        loopLabel.move(30, 90)
        self.loop.move(240, 90)

        qualityLabel.move(30, 120)
        self.quality.move(100, 120)

        timeLabel.move(210, 120)
        self.time.move(360, 120)

        self.outputLine.move(30, 160)
        outputBtn.move(400, 160)

        self.other()

    def other(self):
        self.msg.move(80, 190)
        self.runBtn.move(200, 220)

    def openDialog(self, mode):
        fileDialog = QFileDialog(self.commandUi)
        fileDialog.setWindowTitle("标题")
        fileDialog.setFileMode(mode)
        fileDialog.setDirectory("/")
        fileDialog.setNameFilter("Images (*.png *.jpeg *.jpg *.tiff *.webp)")
        # 窗口显示，返回文件路径
        file_path = fileDialog.exec()

        if file_path and fileDialog.selectedFiles():
            if mode == QFileDialog.DirectoryOnly:
                self.outputLine.setText(fileDialog.selectedFiles()[0])
                log.info("{} 输出路径为：{}".format(self.command, fileDialog.selectedFiles()[0]))
            else:
                self.inputLine.setText(",".join(fileDialog.selectedFiles()))
                log.info("{} 输入路径为：{}".format(self.command, fileDialog.selectedFiles()))

    def check(self):
        input_path = self.inputLine.text()
        output_path = self.outputLine.text()
        if input_path == "":
            self.set_msg("输入文件或文件夹不能为空", Qt.GlobalColor.red)
            return False
        if output_path == "":
            self.set_msg("输出文件夹不能为空", Qt.GlobalColor.red)
            return False
        if self.width.text() == "" and self.height.text():
            self.set_msg("宽和高必须同时输入，或者不输入", Qt.GlobalColor.red)
            return False
        if self.height.text() == "" and self.width.text():
            self.set_msg("宽和高必须同时输入，或者不输入", Qt.GlobalColor.red)
            return False
        if self.time.value() <= 0:
            self.set_msg("每张图片时长不能小于等于0", Qt.GlobalColor.red)
            return False

        cp = CommandParameter(self.command, input_path, output_path)
        cp.set_loop_value(self.loop.value())
        cp.set_quality_value(self.quality.currentText())
        cp.set_time_value(self.time.value())
        if self.width.text() and self.height.text():
            cp.set_width_and_height(self.width.text(), self.height.text())

        self.command_parameter = cp

        return True


class Img2WebpCommand(Command):
    name = "img2webp"
    description = (
        "create animated WebP file from a sequence of input images."
    )

    def handle(self):
        Img2WebpCommandWindow(self.name).command_ui()
