from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import sys

app = QApplication(sys.argv)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My PyQt App")
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel("Hello PyQt", self)
        self.label.setGeometry(150, 100, 200, 50)

        self.button = QPushButton("Click me", self)
        self.button.setGeometry(150, 150, 100, 50)
        self.button.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        self.label.setText("Button Clicked")

if __name__ == '__main__':
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())