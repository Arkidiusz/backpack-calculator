import pytest

import time

from unittest.mock import MagicMock, patch

from src.main_window import *
from src.backpack import Backpack

import re

from PyQt5.QtTest import QTest

@pytest.fixture
def backpack():
    return Backpack()

@pytest.fixture
def main_window(qtbot):
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    return main_window

def test_populate_metrics_table(backpack, main_window):
    # Arrange
    metrics = backpack.compute_metrics()
    
    # Act
    main_window.populate_metrics_table(metrics)
    
    # Assert
    labels = main_window.grid_container.findChildren(QLabel)
    assert len(labels) == len(metrics) * 2
    for row in range(main_window.metrics_grid.rowCount()):
        metric_name = re.sub(':', '', main_window.metrics_grid.itemAtPosition(row, 0).widget().text())
        metric_value = float(main_window.metrics_grid.itemAtPosition(row, 1).widget().text())
        assert f'{metric_name}' in metrics.keys()
        assert metrics[metric_name] == metric_value

def test_add_item_calls_open_popup(qtbot):
    mock_open_popup = MagicMock()
    with patch('src.main_window.MainWindow._open_popup') as mock_open_popup:
        main_window = MainWindow()
        qtbot.mouseClick(main_window.add_item_button, Qt.LeftButton)
        
    assert mock_open_popup.assert_called_once
        