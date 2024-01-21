from src.backpack import Backpack
from src.items import Banana

import pytest
from unittest.mock import MagicMock

@pytest.fixture
def backpack():
    return Backpack()

@pytest.fixture
def banana():
    return Banana()

def test_update_item_new_item(backpack, banana):
    # Arrange
    mock_compute_metrics = MagicMock()
    backpack.compute_metrics = mock_compute_metrics

    # Act
    backpack.update_item(banana)

    # Assert
    assert banana in backpack.items
    assert backpack.items[banana] == banana.get_metrics()
    assert len(backpack.items) == 1
    mock_compute_metrics.assert_called_once()

def test_update_item_existing_item(backpack, banana):
    # TODO implement once updating items is implemented
    pass

def test_compute_metrics(backpack, banana):
    # Act
    backpack.update_item(banana)
    metrics = backpack.compute_metrics()

    # Assert
    assert metrics['sps'] == 1.1875
    assert metrics['hps'] == 0.75
