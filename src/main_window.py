from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QGuiApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Backpack Calculator")

        screen_resolution = QGuiApplication.primaryScreen().geometry()
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
        self.setGeometry(0, 0, screen_width, screen_height)

        # self.label = QLabel("Hello PyQt", self)
        # self.label.setGeometry(150, 100, 200, 50)

        # self.button = QPushButton("Click me", self)
        # self.button.setGeometry(150, 150, 100, 50)
        # self.button.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        self.label.setText("Button Clicked")