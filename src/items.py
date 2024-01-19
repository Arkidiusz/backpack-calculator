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
