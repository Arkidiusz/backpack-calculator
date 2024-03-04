from PyQt5.QtWidgets import QMainWindow, QScrollArea, QVBoxLayout, QWidget, QLabel, QSizePolicy, QGridLayout
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import Qt

from .controller import update_metrics

class MainWindow(QMainWindow):
    """
        Defines the appearance and elements of the application
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Backpack Calculator")
        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        self.setGeometry(0, 0, screen_resolution.width(), screen_resolution.height())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self._create_metrics_table()
        self.populate_metrics_table()
    
    def _create_metrics_table(self) -> None:
        """
            Creates a display column of metrics
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.central_widget.setLayout(layout)
        
        metrics_label = QLabel('Metrics:')

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        scroll_widget.setLayout(self.scroll_layout)
        scroll_area.setWidget(scroll_widget)

        layout.addWidget(metrics_label)
        layout.addWidget(scroll_area)
    
    def populate_metrics_table(self) -> None:
        """
            Updates the metrics table with calculated metrics
        """
        metrics = update_metrics()
        row = 0
        for metric_name, metric_value in metrics.items():
            metric_name_label = QLabel(f'<b>{metric_name}:</b>')
            self.scroll_layout.addWidget(metric_name_label, row, 0, alignment=Qt.AlignRight)
            
            metric_value_label = QLabel(str(metric_value))
            self.scroll_layout.addWidget(metric_value_label, row, 1)

            row += 1
