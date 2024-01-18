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

    def __init__(cls, item_data_path = 'data/items.json'):        
        item_data_file = open(item_data_path)
        cls.item_data = json.load(item_data_file)

        cls.items = {}
        cls.combat_duration = 1

        cls._update_metrics()
    
    def update_item(cls, item : Item) -> None:
        """Updates item metrics/adds a new item to items list and recomputes Backpack metrics

        Attributes:
            :item: an item object 
        """
        metrics = item.get_metrics()
        cls.items[item] = metrics
        cls._update_metrics()
    
    def _update_metrics(cls) -> None:
        """Computes all metrics in the backpack
        """
        
        
        stamina = 0
        healing = 0
        for item, metrics in cls.items.items():
            for metric_name, metric_value in metrics.items():
                match metric_name:
                    case 'stamina':
                        stamina += metric_value
                    case 'healing':
                        healing += metric_value

        cls.sps = cls.BASE_STAMINA_GENERATION + stamina / cls.combat_duration
        cls.hps = healing / cls.combat_duration


class Item:
    """Item represents all properties of an item used to evaluate its value contribution to a backpack

    Attributes:
        backpack: a reference to a Backpack object where item belongs to
        name: name of item
        tags: A list of tags of item such as "food" or "bag"
    """
    def __init__(cls, backpack: Backpack, name: str, tags: list[str]):
        cls.backpack = backpack
        cls.name = name
        cls.tags = tags
    
    def get_metrics(cls) -> dict[str, float]:
        """Computes all metrics contributed by item to a backpack

        :return: a mapping of metrics name and its value
        """
        raise Exception('Abstract function, requires implementation')


class Food:
    """An Item type which scales cooldown with other food of different type

    Attributes:
        adjacent_food: a number of adjecent food of different type
        ADJECENCY_SCALING: an additive cooldown bonus for each adjecent_food, e.g. 3 adjecent items will reduce the cooldown by multiplier of 0.7
    """
    ADJECENCY_SCALING = 0.1

    def __init__(cls, adjacent_food: int = 0):
        cls.adjacent_food = adjacent_food


class Banana(Item, Food):
    """Banana is an item which provides health and stamina regeneration on trigger and scales with other food

    Attributes:
        heal: how much healing it provides on trigger
        stamina_regeneration: how much stamina is regenerated on cooldown
        cooldown: A list of tags of item such as "food" or "bag"
    """

    def __init__(cls, backpack: Backpack):
        banana_data = backpack.item_data['items']['Banana']
        Item.__init__(cls, backpack, 'Banana', banana_data['tags'])
        Food.__init__(cls)
        
        attributes = banana_data['attributes']
        cls.heal = attributes['heal']
        cls.stamina_regeneration = attributes['stamina_regeneration']
        cls.cooldown = attributes['cooldown']
    
    def get_metrics(cls) -> dict[str, float]:
        """
        Metrics:
            healing: total healing item contributes over combat duration
            stamina: total stamina item restores in combat (assuming dicitonary is not capped)
        """
        cooldown = cls.cooldown * (1 - cls.adjecent_food * cls.ADJECENCY_SCALING)
        triggers = cls.backpack.combat_duration // cooldown
        
        metrics = {}

        healing = triggers * cls.heal
        metrics['healing'] = healing

        stamina = triggers * cls.stamina_regeneration   
        metrics['stamina'] = stamina

        return metrics       
