"""This is an interface for providing all configuration information to the application"""

import json

combat_duration = 16
expected_hits = 10
item_data_file = json.load(open("data/items.json", encoding="utf-8"))


def get_combat_duration():
    # TODO refactor to fetch variable directly
    return combat_duration


def get_expected_hits():
    # TODO refactor to fetch variable directly
    return expected_hits


def get_item_data():
    # TODO refactor to fetch variable directly
    return item_data_file


def get_item_names() -> list[str]:
    """Identifies all item names from the json file

    Returns:
        list[str]: a list of all possible item names
    """
    return list(item_data_file["items"].keys())
