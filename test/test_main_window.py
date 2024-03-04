import pytest
from PyQt5.QtWidgets import QApplication

from src.main_window import *
from src.backpack import Backpack


import re

@pytest.fixture
def backpack():
    return Backpack()

@pytest.fixture
def app():
    app = QApplication([])
    yield app
    app.quit()

def test_populate_metrics_table(app, backpack):
    # Arrange
    window = MainWindow()
    metrics = backpack.compute_metrics()
    
    # Act
    window.populate_metrics_table(metrics)
    
    # Assert
    labels = window.grid_container.findChildren(QLabel)
    assert len(labels) == len(metrics) * 2
    for row in range(window.metrics_grid.rowCount()):
        metric_name = re.sub(':', '', window.metrics_grid.itemAtPosition(row, 0).widget().text())
        metric_value = float(window.metrics_grid.itemAtPosition(row, 1).widget().text())
        assert f'{metric_name}' in metrics.keys()
        assert metrics[metric_name] == metric_value
        