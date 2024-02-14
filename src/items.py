from src.controller import *
from src.exceptions import BackpackException

class Item:
    """Item represents all properties of an item used to evaluate its value contribution to a backpack

    Attributes:
        name: name of item
        item_data: a dictionary of all data associated with the item
        tags: a list of tags of item such as "food" or "bag"
        cost: an integer cost of an item
    """
    def __init__(self, name: str):
        self.name = name
        
        self.item_data = get_item_data()['items'][name]
        self.tags = self.item_data['tags']
        self.cost = self.item_data['cost']
    
    def get_metrics(self) -> dict[str, float]:
        """Computes all metrics contributed by item to a backpack

        :return: a mapping of metrics name and its value
        """
        raise BackpackException('Abstract function, requires implementation')


class Food(Item):
    """An Item type which scales cooldown with other food of different type

    Attributes:
        adjacent_food: a number of adjecent food of different type
        cooldown: A list of tags of item such as "food" or "bag"
        ADJECENCY_SCALING: an additive cooldown bonus for each adjecent_food, e.g. 3 adjecent items will reduce the cooldown by multiplier of 0.7
    """
    ADJECENCY_SCALING = 0.1

    def __init__(self, name: str, adjacent_food: int = 1):
        Item.__init__(self, name)
        self.adjacent_food = adjacent_food

        self.cooldown = self.item_data['attributes']['cooldown']


class Banana(Food):
    """Banana is an item which provides health and stamina regeneration on trigger and scales with other food

    Attributes:
        heal: how much healing it provides on trigger
        stamina_regeneration: how much stamina is regenerated on cooldown
    """

    def __init__(self, adjacent_food: int = 1):
        Food.__init__(self, 'Banana', adjacent_food)
        
        attributes = self.item_data['attributes']
        self.heal = attributes['heal']
        self.stamina_regeneration = attributes['stamina_regeneration']
        
    
    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            healing: total healing item contributes over combat duration
            stamina: total stamina item restores in combat (assuming dicitonary is not capped)
        """
        cooldown = self.cooldown * (1 - self.adjacent_food * self.ADJECENCY_SCALING)
        triggers = get_combat_duration() // cooldown
        metrics = {}

        healing = triggers * self.heal
        metrics['healing'] = healing

        stamina = triggers * self.stamina_regeneration   
        metrics['stamina'] = stamina

        return metrics
    

class Garlic(Food):
    """Garlic is an item which provides armor and vampirism removal on trigger

        Attributes:
            armor_generation: how much armor it provides on trigger
            vampirism_removal: how much vampirism is removed on trigger
            vamprism_removal_chance: chance to remove vampirism on trigger
    """

    def __init__(self, adjacent_food: int = 1):
        Food.__init__(self, 'Garlic', adjacent_food)
        
        attributes = self.item_data['attributes']
        self.armor_generation = attributes['armor_generation']
        self.vampirism_removal = attributes['vampirism_removal']
        self.vamprism_removal_chance = attributes['vamprism_removal_chance']


class Weapon(Item):
    """ Item Type which deals damage on trigger

    Attributes:
        minimum_damage: minimum damage dealt on trigger
        maximum_damage: maximum damage dealt on trigger
        cooldown: frequency of triggers
        accuracy: chance to deal damage on trigger
        stamina_cost: cost of stamina on trigger
    """

    def __init__(self, name: str):
        Item.__init__(self, name)
        
        attributes = self.item_data['attributes']
        self.minimum_damage = attributes['minimum_damage']
        self.maximum_damage = attributes['maximum_damage']
        self.cooldown = attributes['cooldown']
        self.accuracy = attributes['accuracy']
        self.stamina_cost = attributes['stamina_cost']

class WoodenSword(Weapon):
    """WoodenSword is a basic melee weapon
    """

    def __init__(self):
        Weapon.__init__(self, 'Wooden Sword')
    
    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            damage: expected total damage assuming enough stamina
            stamina_cost: expected total stamina cost
        """
        triggers = get_combat_duration() // self.cooldown
        metrics = {}

        damage = triggers * self.accuracy * (sum([self.minimum_damage, self.maximum_damage]) / 2)
        metrics['damage'] = damage 

        stamina_cost = triggers * self.stamina_cost
        metrics['stamina_cost'] = stamina_cost

        return metrics       

class Pan(Weapon):
    """Pan is a basic melee weapon scaling with adjacent Food items

    Attributes:
        adjacent_foods: number of adjacent food items
        damage_bonus: how much damage each adjacent food contributes
    """

    def __init__(self, adjacent_foods = 1):
        Weapon.__init__(self, 'Pan')
        
        attributes = self.item_data['attributes']
        self.damage_bonus = attributes['damage_bonus']
        self.adjacent_foods = adjacent_foods
    
    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            damage: expected total damage assuming enough stamina
            stamina_cost: expected total stamina cost
        """
        triggers = get_combat_duration() // self.cooldown
        metrics = {}

        minimum_damage = self.minimum_damage + self.adjacent_foods * self.damage_bonus
        maximum_damage = self.maximum_damage + self.adjacent_foods * self.damage_bonus
        damage = triggers * self.accuracy * (sum([minimum_damage, maximum_damage]) / 2)
        metrics['damage'] = damage 

        stamina_cost = triggers * self.stamina_cost
        metrics['stamina_cost'] = stamina_cost

        return metrics
    