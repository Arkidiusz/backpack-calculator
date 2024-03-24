from .backpack import Backpack
import src.config as config
from .items import *

backpack = Backpack()


def request_metrics_update() -> dict[str, float]:
    """Requests backpack to recompute its metrics

    :return: a dictionary mapping of metric name to its value
    """
    return backpack.compute_metrics()


def add_item(item_name: str) -> dict[str, float]:
    """Creates and Item object based on the provided string, adds item to backpack and calls for recalculation of metrics

    Args:
        item_name (str): a name of item as displayed in the gui

    Returns:
        dict[str, float]: a mapping of item names to their value
    """
    item = None
    match item_name:
        case "Banana":
            item = Banana()
        case "Wooden Sword":
            item = WoodenSword()
        case "Stone":
            item = Stone()
        case "Pan":
            item = Pan()
        case "Wooden Buckler":
            item = WoodenBuckler()
        case "Garlic":
            item = Garlic()
        case "Healing Herbs":
            item = HealingHerbs()
        case "Walrus Tusk":
            item = WalrusTusk()
        case "Pocket Sand":
            item = PocketSand()
    backpack.items[item] = item.get_metrics()
    metrics = backpack.compute_metrics()
    return metrics


def delete_item(item_name: str) -> None:
    """Removes an item from the backpack based on its name

    Args:
        item_name (str): name identifying item
    """
    for item in backpack.items.keys():
        if item.name == item_name:
            del backpack.items[item]
            break


def set_combat_duration(combat_duration: int) -> dict[str, float]:
    """Sets combat_duration and notifies backpack to provide updates

    Args:
        combat_duration (int): duration of the combat

    Returns:
        dict[str, float]: returns a set of updated metrics
    """
    config.combat_duration = combat_duration
    backpack.update_items()
    return request_metrics_update()


def get_combat_duration() -> int:
    """Returns combat duration

    Returns:
        int: combat duration
    """
    return combat_duration
