import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from ImgWebp.utils.script import LibWebp
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt


class MyWindow:
    def __init__(self, command):
        self.command = command

    def command_ui(self):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling,True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

        app = QApplication(sys.argv)
        self.set_ui()
        sys.exit(app.exec_())

    def set_ui(self):
        pass


class CommandUi(QWidget):
    def __init__(self, command):
        super().__init__()
        self.resize(600, 400)
        self.setWindowTitle(f"{command}操作界面")


class CommandWindow(MyWindow):
    def __init__(self, command):
        super().__init__(command)
        self.command_parameter = None

    def set_ui(self):
        self.commandUi = CommandUi(self.command)
        self.commandUi.resize(600, 260)

        self.msg = QLabel("", self.commandUi)
        self.msg.resize(300, 30)
        self.msg.move(80, 150)

        self.runBtn = QPushButton("执行", self.commandUi)
        self.runBtn.resize(150, 40)
        self.runBtn.move(200, 180)
        self.runBtn.clicked.connect(self.run)

        self.set_input_btn()

        self.set_output_btn()

        self.commandUi.show()

    def set_msg(self,msg, msg_type):
        if msg:
            self.msg.setText(msg)
            palette = QPalette()
            palette.setColor(palette.WindowText, msg_type)
            self.msg.setPalette(palette)
        else:
            self.msg.setText("")
    def set_input_btn(self):
        pass

    def set_output_btn(self):
        pass

    def check(self) -> bool:
        pass

    def run(self):
        if not self.check():
            return

        lw = LibWebp(self.command, self.command_parameter)
        lw.run()
        if lw.success:
            self.set_msg("执行成功", Qt.GlobalColor.green)


if __name__ == "__main__":
    cwebpWindow = CommandWindow("cwebp")
    cwebpWindow.command_ui()
