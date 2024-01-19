from src.backpack import Backpack
from src.items import Banana
from unittest.mock import MagicMock

def test_update_item_new_item():
    # Arrange
    mock_update_metrics = MagicMock()
    backpack = Backpack()
    backpack._update_metrics = mock_update_metrics
    banana = Banana()
    metrics = banana.get_metrics()

    # Act
    backpack.update_item(banana)

    # Assert
    assert banana in backpack.items
    assert backpack.items[banana] == metrics
    mock_update_metrics.assert_called_once()
