from src.items import Banana
import src.controller as controller

from unittest.mock import MagicMock

import pytest

@pytest.fixture(autouse=True)
def setup():
    controller.backpack = controller.Backpack()
    
def test_add_item():
    # Act
    controller.add_item('Banana')

    # Assert
    assert len(controller.backpack.items) == 1
    assert isinstance(list(controller.backpack.items.keys())[0], Banana)

def test_delete_item():
    assert len(controller.backpack.items) == 0
    # Arrange
    controller.add_item('Banana')

    # Act
    controller.delete_item('Banana')
    
    # Assert
    assert len(controller.backpack.items) == 0