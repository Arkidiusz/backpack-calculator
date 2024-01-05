class Backpack:
    """Represents all information in a backpack used to calculate its value

    Attributes:
        items: a list of items in a backpack
    """
    def __init__(cls, items: List[Item] = []) -> None:
        cls.items = items

class Item:
    """Item represents all properties of an item used to evaluate its value contribution to a backpack

    Attributes:
        name: name of item
        tags: A list of tags of item such as "food" or "bag"
    """
    def __init__(cls, name: str, tags: List[str]) -> None:
        cls.name = name
        cls.tags = tags

def add_numbers(a, b):
    print("running main.py")
    return a + b
