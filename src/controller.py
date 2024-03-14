from .backpack import Backpack
from .items import *

backpack = Backpack()

def request_metrics_update() -> dict[str, float]:
    """Requests backpack to recompute its metrics
        
    :return: a dictionary mapping of metric name to its value
    """
    return backpack.compute_metrics()

def add_item(item_name: str) -> dict[str, float]:
    item = None
    match item_name:
        case 'Banana':
            item = Banana()
        case 'Wooden Sword':
            item = WoodenSword()
        case 'Stone':
            item = Stone()
        case 'Pan':
            item = Pan()
        case 'Wooden Buckler':
            item = WoodenBuckler()
        case 'Garlic':
            item = Garlic()
        case 'Healing Herbs':
            item = HealingHerbs()
        case 'Walrus Tusk':
            item = WalrusTusk()
        case 'Pocket Sand':
            item = PocketSand()
    backpack.items[item] = item.get_metrics()
    metrics = backpack.compute_metrics()
    return metrics
