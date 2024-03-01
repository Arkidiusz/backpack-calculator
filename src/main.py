from PyQt5.QtWidgets import QApplication
import sys
from main_window import MainWindow

app = QApplication(sys.argv)

if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())