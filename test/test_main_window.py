import pytest

from unittest.mock import MagicMock, patch

from src.main_window import *
from src.backpack import Backpack
import src.controller as controller

import re


@pytest.fixture
def backpack():
    return Backpack()


@pytest.fixture
def main_window(qtbot):
    return MainWindow()


@pytest.fixture
def combat_duration():
    return controller.get_combat_duration() + 1


def test_populate_metrics_table(backpack, main_window):
    # Arrange
    metrics = backpack.compute_metrics()

    # Act
    main_window.populate_metrics_table(metrics)

    # Assert
    labels = main_window.grid_container.findChildren(QLabel)
    assert len(labels) == len(metrics) * 2
    for row in range(main_window.metrics_grid.rowCount()):
        metric_name = re.sub(
            ":", "", main_window.metrics_grid.itemAtPosition(row, 0).widget().text()
        )
        metric_value = float(
            main_window.metrics_grid.itemAtPosition(row, 1).widget().text()
        )
        assert f"{metric_name}" in metrics.keys()
        assert metrics[metric_name] == metric_value


def test_add_item_button_clicked(qtbot):
    # Arrange
    mock_open_popup = MagicMock()

    # Act
    with patch("src.main_window.MainWindow._open_popup") as mock_open_popup:
        main_window = MainWindow()
        qtbot.mouseClick(main_window.add_item_button, Qt.LeftButton)

    # Assert
    mock_open_popup.assert_called_once()


def test_ok_button_clicked(qtbot):
    # Arrange
    mock_add_items = MagicMock()
    mock_populate_metrics_table = MagicMock()
    with patch("src.main_window.controller.add_item", autospec=True) as mock_add_items:
        main_window = MainWindow()
        main_window.populate_metrics_table = mock_populate_metrics_table
        add_item_popup = AddItemPopup(main_window)
        add_item_popup.items_combo_box.setCurrentText("Wooden Sword")

        # Act
        qtbot.mouseClick(add_item_popup.ok_button, Qt.LeftButton)

    # Assert
    mock_add_items.assert_called_with("Wooden Sword")
    mock_populate_metrics_table.assert_called_once()
    assert main_window.item_list_widget.count() == 1


def test_items_combo_box(main_window):
    # Arrange
    add_item_popup = AddItemPopup(main_window)

    # Assert
    items = controller.get_item_names()
    for i in range(len(items)):
        assert items[i] == add_item_popup.items_combo_box.itemText(i)


def test_delete_item(main_window, qtbot):
    # Arrange
    add_item_popup = AddItemPopup(main_window)
    add_item_popup._add_item()
    populate_metrics_mock = MagicMock()
    main_window.populate_metrics_table = populate_metrics_mock
    items = main_window.item_list_widget.findItems("Banana", Qt.MatchFixedString)
    items[0].setSelected(True)

    # Act
    qtbot.mouseClick(main_window.delete_item_button, Qt.LeftButton)

    # Assert
    assert controller.backpack.items == {}
    populate_metrics_mock.assert_called_once()


def test_click_combat_duration_spinner(qtbot, combat_duration):
    # Arrange
    # combat_duration = controller.get_combat_duration() + 1
    with patch(
        "src.main_window.MainWindow._update_combat_duration", autospec=False
    ) as mock_update_combat_duration:
        main_window = MainWindow()
        spinner = main_window.combat_duration_spinner

        # Act
        spinner.setValue(combat_duration)

    # Assert
    assert spinner.value() == combat_duration
    mock_update_combat_duration.assert_called_with(combat_duration)


@patch("src.main_window.MainWindow.populate_metrics_table")
@patch("src.main_window.controller.set_combat_duration")
def test_update_combat_duration(
    set_combat_duration_mock, populate_metrics_table_mock, combat_duration
):
    # Arrange
    main_window = MainWindow()

    # Act
    main_window._update_combat_duration(combat_duration)

    # Assert
    set_combat_duration_mock.assert_called_with(combat_duration)
    assert populate_metrics_table_mock.call_count == 2
