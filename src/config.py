import json

combat_duration = 16
expected_hits = 10
item_data_file = json.load(open('data/items.json', encoding='utf-8'))

def get_combat_duration():
    return combat_duration

def get_expected_hits():
    return expected_hits

def get_item_data():
    return item_data_file

def get_item_names() -> list[str]:
    """Identifies all item names from the json file

    :return: a list of all possible item names
    """
    return list(item_data_file["items"].keys())