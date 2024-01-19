import json

def add_numbers(a, b):
    "This is just for testing - to be removed"
    
    print("running main.py")
    return a + b


class Backpack:
    """Represents all information in a backpack used to calculate its value

    Attributes:
        item_data: a json file containing item data
        items: a dictionary mapping of 
    """

    BASE_STAMINA_GENERATION = 1

    def __init__(self, item_data_path = 'data/items.json'):        
        item_data_file = open(item_data_path)
        self.item_data = json.load(item_data_file)

        self.items = {}
        self.combat_duration = 1

        self._update_metrics()
    
    def update_item(self, item : Item) -> None:
        """Updates item metrics/adds a new item to items list and recomputes Backpack metrics

        Attributes:
            :item: an item object 
        """

        metrics = item.get_metrics()
        self.items[item] = metrics
        self._update_metrics()
    
    def _update_metrics(self) -> None:
        """Computes and updates all metrics in the backpack
        """
        
        stamina = 0
        healing = 0
        for item, metrics in self.items.items():
            for metric_name, metric_value in metrics.items():
                match metric_name:
                    case 'stamina':
                        stamina += metric_value
                    case 'healing':
                        healing += metric_value

        self.sps = self.BASE_STAMINA_GENERATION + stamina / self.combat_duration
        self.hps = healing / self.combat_duration


class Item:
    """Item represents all properties of an item used to evaluate its value contribution to a backpack

    Attributes:
        backpack: a reference to a Backpack object where item belongs to
        name: name of item
        tags: A list of tags of item such as "food" or "bag"
    """
    def __init__(self, backpack: Backpack, name: str, tags: list[str]):
        self.backpack = backpack
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

    def __init__(self, backpack: Backpack):
        banana_data = backpack.item_data['items']['Banana']
        Item.__init__(self, backpack, 'Banana', banana_data['tags'])
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
        triggers = self.backpack.combat_duration // cooldown
        
        metrics = {}

        healing = triggers * self.heal
        metrics['healing'] = healing

        stamina = triggers * self.stamina_regeneration   
        metrics['stamina'] = stamina

        return metrics       

class BackpackException(Exception):
    """ A base class for all exception related to Backpack errors
    """
