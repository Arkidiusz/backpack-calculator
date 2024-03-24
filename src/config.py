"""This is an interface for providing all configuration information to the application"""

import json

combat_duration = 16
expected_hits = 10
item_data = json.load(open("data/items.json", encoding="utf-8"))["items"]


def get_item_names() -> list[str]:
    """Identifies all item names from the json file

    Returns:
        list[str]: a list of all possible item names
    """
    return list(item_data.keys())
