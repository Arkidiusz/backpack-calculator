from src.items import *
from src.controller import get_item_data

import pytest

@pytest.fixture
def item_name():
    return 'tast-name'

@pytest.fixture
def item_tags():
    return ['tast-tag']

def test_create_item(item_name, item_tags):
    # Act
    item = Item(item_name, item_tags)

    # Assert
    assert item.name == item_name
    assert item.tags == item_tags

def test_get_metrics_raises(item_name, item_tags):
    # Except
    item = Item(item_name, item_tags)
    with pytest.raises(BackpackException):
        item.get_metrics()

def test_create_banana():
    # Arrange
    attributes = get_item_data()['items']['Banana']['attributes']

    # Act
    banana = Banana()

    # Assert
    banana.heal = attributes['heal']
    banana.stamina_regeneration = attributes['stamina_regeneration']
    banana.cooldown = attributes['cooldown']

def test_banana_get_metrics():
    # Arrange
    attributes = get_item_data()['items']['Banana']['attributes']

    # Act
    banana = Banana()
    metrics = banana.get_metrics()

    # Assert
    assert metrics['healing'] == 12
    assert metrics['stamina'] == 3

def test_create_wooden_sword():
    # Arrange
    attributes = get_item_data()['items']['Wooden Sword']['attributes']

    # Act
    sword = WoodenSword()

    # Assert
    sword.minimum_damage = attributes['minimum_damage']
    sword.maximum_damage = attributes['maximum_damage']
    sword.cooldown = attributes['cooldown']
    sword.accuracy = attributes['accuracy']
    sword.stamina_cost = attributes['stamina_cost']

def test_wooden_sword_get_metrics():
    # Arrange
    attributes = get_item_data()['items']['Wooden Sword']['attributes']

    # Act
    sword = WoodenSword()
    metrics = sword.get_metrics()

    # Assert
    assert metrics['damage'] == 18.0
    assert metrics['stamina_cost'] == 7.699999999999999
