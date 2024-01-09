class Item:
    """Item represents all properties of an item used to evaluate its value contribution to a backpack

    Attributes:
        name: name of item
        tags: A list of tags of item such as "food" or "bag"
    """
    def __init__(cls, name: str = "Item", tags: list[str] = []) -> None:
        cls.name = name
        cls.tags = tags

class Banana(Item):
    """Item represents all properties of an item used to evaluate its value contribution to a backpack

    Attributes:
        name: name of item
        tags: A list of tags of item such as "food" or "bag"
    """
    ENERGY_GENERATION = 0.2
    HEALTH_GENERATION = 0.5

    def __init__(cls, name: str = "Banana", tags: list[str] = []) -> None:
        super.__init__(name, tags)
        cls.name = name
        cls.tags = tags
    