from src.items import Item

def add_numbers(a, b):
    "This is just for testing - to be removed"
    
    print("running main.py")
    return a + b

class Backpack:
    """Represents all information in a backpack used to calculate its value

    Attributes:
        items: a list of items in a backpack
    """
    def __init__(cls, items: list[Item] = []) -> None:
        cls.items = items
