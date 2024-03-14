from PyQt5.QtWidgets import QMainWindow, QScrollArea, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSizePolicy, QGridLayout, QPushButton, QDialog, QComboBox
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import Qt

from .controller import request_metrics_update, add_item
from .config import get_item_names

class MainWindow(QMainWindow):
    """Defines the appearance and elements of the application
    """
    def __init__(self):
        """Initialise main window, its central widget, layout and call functions to create all widgets and components of this window
        """
        super().__init__()

        self.setWindowTitle("Backpack Calculator")
        screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
        self.setGeometry(0, 0, screen_resolution.width(), screen_resolution.height())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.central_layout = QHBoxLayout()
        self.central_layout.setAlignment(Qt.AlignLeft)
        central_widget.setLayout(self.central_layout)

        self._create_metrics_table()
        self._create_add_item_button()
    
    def _create_metrics_table(self) -> None:
        """Creates a display column of metrics
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)
        self.central_layout.addWidget(widget)
        
        metrics_label = QLabel('Metrics:')

        self.grid_container = QWidget()
        self.metrics_grid = QGridLayout(self.grid_container)
        self.metrics_grid.setAlignment(Qt.AlignTop)
        self.grid_container.setLayout(self.metrics_grid)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        scroll_area.setWidget(self.grid_container)

        layout.addWidget(metrics_label)
        layout.addWidget(scroll_area)

        self.populate_metrics_table(request_metrics_update())
    
    def populate_metrics_table(self, metrics: dict[str, float]) -> None:
        """Updates the metrics table with provided metrics
        
        Attributes:
            metrics: a mapping of metric name to its float value
        """
        # clear the grid
        for i in reversed(range(self.metrics_grid.count())): 
            self.metrics_grid.itemAt(i).widget().setParent(None)

        row = 0
        for metric_name, metric_value in metrics.items():
            metric_name_label = QLabel(f'{metric_name}:')
            self.metrics_grid.addWidget(metric_name_label, row, 0, alignment=Qt.AlignRight)
            
            metric_value_label = QLabel(str(metric_value))
            self.metrics_grid.addWidget(metric_value_label, row, 1)

            row += 1

    def _create_add_item_button(self):
        """ A button for adding new items to the backpack
        """
        button = QPushButton("Add Item")
        button.clicked.connect(self._open_popup)
        self.central_layout.addWidget(button)   
    
    def _open_popup(self):
        """ A popup window enabling item selection
        """
        popup = QDialog()
        popup.setWindowTitle("Add Item")
        popup.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        popup.accepted.connect(self._add_item)
        
        layout = QVBoxLayout()
        popup.setLayout(layout)

        self.items_combo_box = QComboBox()
        self.items_combo_box.addItems(get_item_names())
        
        ok_button = QPushButton("Add Item")
        ok_button.clicked.connect(popup.accept)

        layout.addWidget(self.items_combo_box)
        layout.addWidget(ok_button)

        popup.exec_()
    
    def _add_item(self) -> None:
        metrics = add_item(self.items_combo_box.currentText())
        self.populate_metrics_table(metrics)
