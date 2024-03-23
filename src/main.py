from PyQt5.QtWidgets import QApplication

import sys

from .main_window import MainWindow

from .controller import *


if __name__ == "__main__":
    """Entry point of the application initialising main_window creation"""
    app = QApplication(sys.argv)
    with open('style/Cstartpage.qss', 'r') as f:
        app.setStyleSheet(f.read())
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
