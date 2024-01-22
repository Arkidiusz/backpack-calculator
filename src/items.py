from src.controller import *
from src.exceptions import BackpackException

class Item:
    """Item represents all properties of an item used to evaluate its value contribution to a backpack

    Attributes:
        name: name of item
        tags: A list of tags of item such as "food" or "bag"
    """
    def __init__(self, name: str, tags: list[str]):
        self.name = name
        self.tags = tags
    
    def get_metrics(self) -> dict[str, float]:
        """Computes all metrics contributed by item to a backpack

        :return: a mapping of metrics name and its value
        """
        raise BackpackException('Abstract function, requires implementation')


class Food:
    """An Item type which scales cooldown with other food of different type

    Attributes:
        adjacent_food: a number of adjecent food of different type
        ADJECENCY_SCALING: an additive cooldown bonus for each adjecent_food, e.g. 3 adjecent items will reduce the cooldown by multiplier of 0.7
    """
    ADJECENCY_SCALING = 0.1

    def __init__(self, adjacent_food: int = 0):
        self.adjacent_food = adjacent_food


class Banana(Item, Food):
    """Banana is an item which provides health and stamina regeneration on trigger and scales with other food

    Attributes:
        heal: how much healing it provides on trigger
        stamina_regeneration: how much stamina is regenerated on cooldown
        cooldown: A list of tags of item such as "food" or "bag"
    """

    def __init__(self):
        banana_data = get_item_data()['items']['Banana']
        Item.__init__(self, 'Banana', banana_data['tags'])
        Food.__init__(self)
        
        attributes = banana_data['attributes']
        self.heal = attributes['heal']
        self.stamina_regeneration = attributes['stamina_regeneration']
        self.cooldown = attributes['cooldown']
    
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

class WoodenSword(Item):
    """WoodenSword is a basic melee weapon

    Attributes:
        minimum_damage: minimum damage dealt on trigger
        maximum_damage: maximum damage dealt on trigger
        cooldown: frequency of triggers
        accuracy: chance to deal damage on trigger
        stamina_cost: cost of stamina on trigger
    """

    def __init__(self):
        sword_data = get_item_data()['items']['Wooden Sword']
        Item.__init__(self, 'Wooden Sword', sword_data['tags'])
        
        attributes = sword_data['attributes']
        self.minimum_damage = attributes['minimum_damage']
        self.maximum_damage = attributes['maximum_damage']
        self.cooldown = attributes['cooldown']
        self.accuracy = attributes['accuracy']
        self.stamina_cost = attributes['stamina_cost']
    
    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            damage: expected total damage assuming enough stamina
            stamina_cost: expected total stamina cost
        """
        cooldown = self.cooldown
        triggers = get_combat_duration() // cooldown
        print(triggers)
        metrics = {}

        damage = int(triggers * self.accuracy) * (sum([self.minimum_damage, self.maximum_damage]) / 2)
        metrics['damage'] = damage 

        stamina_cost = triggers * self.stamina_cost
        metrics['stamina_cost'] = stamina_cost

        return metrics       
