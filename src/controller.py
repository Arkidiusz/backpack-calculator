"""parse item data"""
import json
import src.backpack
import src.items


combat_duration = 16

def get_item_data():
    item_data_file = open('data/items.json', encoding='utf-8')
    return json.load(item_data_file)

def get_combat_duration():
    return combat_duration
