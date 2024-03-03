from PyQt5.QtWidgets import QMainWindow, QScrollArea, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QGuiApplication
from .controller import update_metrics

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Backpack Calculator")

        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
        self.setGeometry(0, 0, screen_width, screen_height)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.layout.addWidget(self.scroll_area)

        # Example data (you can update this dynamically)
        data = {
            "Key 1": "Value 1",
            "Key 2": "Value 2",
            "Key 3": "Value 3"
        }

        self.populate_metrics(data)
    
    def populate_metrics(self, data):
        metrics = update_metrics()
        for key, value in metrics.items():
            label = QLabel(f"<b>{key}:</b> {value}")
            self.scroll_layout.addWidget(label)
