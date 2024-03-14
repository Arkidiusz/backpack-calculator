from src.items import Banana
from src.controller import *

from unittest.mock import MagicMock

def test_add_item():
    # Act
    add_item('Banana')

    # Assert
    assert len(backpack.items) == 1
    assert isinstance(list(backpack.items.keys())[0], Banana)
