from src.items import Banana
import src.controller as controller
import src.config as config

from unittest.mock import MagicMock

import pytest


@pytest.fixture(autouse=True)
def setup():
    """This ensures a clean controller and config for each test case"""
    controller.backpack = controller.Backpack()
    config.combat_duration = 16
    # TODO remove after refactoring controller and config


def test_add_item():
    # Act
    controller.add_item("Banana")

    # Assert
    assert len(controller.backpack.items) == 1
    assert isinstance(list(controller.backpack.items.keys())[0], Banana)


def test_delete_item():
    # Arrange
    controller.add_item("Banana")

    # Act
    controller.delete_item("Banana")

    # Assert
    assert len(controller.backpack.items) == 0


def test_set_combat_duration():
    # Arrange
    combat_duration = config.get_combat_duration() * 2
    previous_metrics = controller.request_metrics_update()

    # Act
    metrics = controller.set_combat_duration(combat_duration)

    # Assert
    assert config.combat_duration == combat_duration

    assert metrics != previous_metrics
    assert metrics == controller.request_metrics_update()
