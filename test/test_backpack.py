from src.backpack import Backpack
from src.items import Banana, WoodenSword, Garlic, Stone, HealingHerbs

import pytest
from unittest.mock import MagicMock

@pytest.fixture
def backpack():
    return Backpack()

@pytest.fixture
def banana():
    return Banana()

@pytest.fixture
def wooden_sword():
    return WoodenSword()

@pytest.fixture
def garlic():
    return Garlic()

@pytest.fixture
def stone():
    return Stone()

@pytest.fixture
def healing_herbs():
    return HealingHerbs()

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

def test_update_item_existing_item(backpack, banana,):
    # TODO implement once updating items is implemented
    pass

def test_compute_metrics(backpack, banana, wooden_sword, garlic, stone, healing_herbs):
    # Act
    backpack.update_item(banana)
    backpack.update_item(wooden_sword)
    backpack.update_item(garlic)
    backpack.update_item(stone)
    backpack.update_item(healing_herbs)
    metrics = backpack.compute_metrics()

    # Assert
    assert metrics['sps'] == 1.02
    assert metrics['hps'] == 1.75
    assert metrics['dps'] == 1.36
    assert metrics['armor'] == 12
    assert metrics['vampirism_removal'] == 1.2
    assert round(metrics['armor_destruction'] , 2) == 1.95
    assert metrics['blind'] == 0

def test_update_metrics(backpack, banana):
    # Act
    backpack.update_item(banana)
    metrics = backpack.compute_metrics()
    backpack.sps = -1
    backpack.hps = -1
    backpack._update_metrics(metrics)

    # Assert
    backpack.sps == metrics['sps']
    backpack.hps == metrics['hps']
