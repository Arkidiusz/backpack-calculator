from src.items import *
from src.controller import get_item_data

import pytest

@pytest.fixture
def item_name():
    return 'Wooden Sword'

@pytest.fixture
def item_tags():
    return ['Melee Weapon']

@pytest.fixture
def item_cost():
    return 3

def test_create_item(item_name, item_tags, item_cost):
    # Act
    item = Item(item_name)

    # Assert
    assert item.name == item_name
    assert item.tags == item_tags
    assert item.cost == item_cost

def test_get_metrics_raises(item_name):
    # Except
    item = Item(item_name)
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

def test_create_garlic():
    # Arrange
    attributes = get_item_data()['items']['Garlic']['attributes']

    # Act
    garlic = Garlic()

    # Assert
    garlic.armor_generation = attributes['armor_generation']
    garlic.vampirism_removal = attributes['vampirism_removal']
    garlic.vamprism_removal_chance = attributes['vamprism_removal_chance']

def test_garlic_get_metrics():
    # Arrange
    attributes = get_item_data()['items']['Garlic']['attributes']

    # Act
    garlic = Garlic()
    metrics = garlic.get_metrics()

    # Assert
    assert metrics['armor'] == 12
    assert metrics['vampirism_removal'] == 1.2

def test_create_wooden_sword():
    # Arrange
    attributes = get_item_data()['items']['Wooden Sword']['attributes']

    # Act
    sword = WoodenSword()

    # Assert
    assert sword.minimum_damage == attributes['minimum_damage']
    assert sword.maximum_damage == attributes['maximum_damage']
    assert sword.cooldown == attributes['cooldown']
    assert sword.accuracy == attributes['accuracy']
    assert sword.stamina_cost == attributes['stamina_cost']

def test_wooden_sword_get_metrics():
    # Arrange
    attributes = get_item_data()['items']['Wooden Sword']['attributes']

    # Act
    sword = WoodenSword()
    metrics = sword.get_metrics()

    # Assert
    assert metrics['damage'] == 19.8
    assert round(metrics['stamina_cost'], 2) == 7.7

def test_create_pan():
    # Arrange
    attributes = get_item_data()['items']['Pan']['attributes']
    adjacent_foods = 4

    # Act
    pan = Pan(adjacent_foods)

    # Assert
    assert pan.minimum_damage == attributes['minimum_damage']
    assert pan.maximum_damage == attributes['maximum_damage']
    assert pan.cooldown == attributes['cooldown']
    assert pan.accuracy == attributes['accuracy']
    assert pan.stamina_cost == attributes['stamina_cost']
    assert pan.damage_bonus == attributes['damage_bonus']
    assert pan.adjacent_foods == adjacent_foods

def test_pan_get_metrics():
    # Arrange
    adjacent_foods = 2

    # Act
    pan = Pan(adjacent_foods)
    metrics = pan.get_metrics()

    # Assert
    assert metrics['damage'] == 32.725
    assert metrics['stamina_cost'] == 6.3

def test_create_stone():
    # Arrange
    attributes = get_item_data()['items']['Stone']['attributes']
    bag_of_marbles = True

    # Act
    stone = Stone(bag_of_marbles)

    # Assert
    assert stone.minimum_damage == attributes['minimum_damage']
    assert stone.maximum_damage == attributes['maximum_damage']
    assert stone.cooldown == attributes['cooldown']
    assert stone.accuracy == attributes['accuracy']
    assert stone.stamina_cost == attributes['stamina_cost']
    assert stone.armor_destruction == attributes['armor_destruction']
    assert stone.bag_of_marbles == bag_of_marbles

def test_stone_get_metrics():
    # Arrange
    adjacent_foods = 2

    # Act
    stone = Stone()
    metrics = stone.get_metrics()

    # Assert
    assert round(metrics['damage'] , 2) == 1.95
    assert metrics['stamina_cost'] == 0
    assert round(metrics['armor_destruction'] , 2) == 1.95

def test_create_healing_herbs():
    # Arrange
    attributes = get_item_data()['items']['Healing Herbs']['attributes']

    # Act
    healing_herbs = HealingHerbs()

    # Assert
    assert healing_herbs.regeneration == attributes['regeneration']

def test_healing_herbs_get_metrics():
    # Act
    stone = HealingHerbs()
    metrics = stone.get_metrics()

    # Assert
    assert metrics['regeneration'] == 2
