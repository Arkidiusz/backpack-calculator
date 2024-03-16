from .config import *
from .exceptions import BackpackException


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

        self.item_data = get_item_data()["items"][name]
        self.tags = self.item_data["tags"]
        self.cost = self.item_data["cost"]

    def get_metrics(self) -> dict[str, float]:
        """Computes all metrics contributed by item to a backpack

        :return: a mapping of metrics name and its value
        """
        raise BackpackException("Abstract function, requires implementation")


class Food(Item):
    """An Item type which scales cooldown with other food of different type

    Attributes:
        adjacent_food: a number of adjacent food of different type
        cooldown: A list of tags of item such as "food" or "bag"
        ADJACENCY_SCALING: an additive cooldown bonus for each adjacent_food, e.g. 3 adjacent items will reduce the cooldown by multiplier of 0.7
    """

    ADJACENCY_SCALING = 0.1

    def __init__(self, name: str, adjacent_food: int = 1) -> None:
        Item.__init__(self, name)
        self.adjacent_food = adjacent_food

        self.cooldown = self.item_data["attributes"]["cooldown"]


class Banana(Food):
    """Banana is an item which provides health and stamina regeneration on trigger and scales with other food

    Attributes:
        heal: how much healing it provides on trigger
        stamina_regeneration: how much stamina is regenerated on cooldown
    """

    def __init__(self, adjacent_food: int = 1):
        Food.__init__(self, "Banana", adjacent_food)

        attributes = self.item_data["attributes"]
        self.heal = attributes["heal"]
        self.stamina_regeneration = attributes["stamina_regeneration"]

    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            healing: total healing item contributes over combat duration
            stamina: total stamina item restores in combat (assuming dictionary is not capped)
        """
        cooldown = self.cooldown * (1 - self.adjacent_food * self.ADJACENCY_SCALING)
        triggers = get_combat_duration() // cooldown

        healing = triggers * self.heal

        stamina = triggers * self.stamina_regeneration

        metrics = {}
        metrics["healing"] = healing
        metrics["stamina"] = stamina

        return metrics


class Garlic(Food):
    """Garlic is an item which provides armor and vampirism removal on trigger

    Attributes:
        armor_generation: how much armor it provides on trigger
        vampirism_removal: how much vampirism is removed on trigger
        vampirism_removal_chance: chance to remove vampirism on trigger
    """

    def __init__(self, adjacent_food: int = 1):
        Food.__init__(self, "Garlic", adjacent_food)

        attributes = self.item_data["attributes"]
        self.armor_generation = attributes["armor_generation"]
        self.vampirism_removal = attributes["vampirism_removal"]
        self.vampirism_removal_chance = attributes["vampirism_removal_chance"]

    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            armor: total armor item contributes over the combat duration
            vampirism_removal: total vampirism item removes over the combat duration
        """
        cooldown = self.cooldown * (1 - self.adjacent_food * self.ADJACENCY_SCALING)
        triggers = get_combat_duration() // cooldown

        armor = triggers * self.armor_generation

        vampirism_removal = (
            triggers * self.vampirism_removal_chance * self.vampirism_removal
        )

        metrics = {}
        metrics["armor"] = armor
        metrics["vampirism_removal"] = vampirism_removal

        return metrics


class Weapon(Item):
    """Item Type which deals damage on trigger

    Attributes:
        minimum_damage: minimum damage dealt on trigger
        maximum_damage: maximum damage dealt on trigger
        cooldown: frequency of triggers
        accuracy: chance to deal damage on trigger
        stamina_cost: cost of stamina on trigger
    """

    def __init__(self, name: str):
        Item.__init__(self, name)

        attributes = self.item_data["attributes"]
        self.minimum_damage = attributes["minimum_damage"]
        self.maximum_damage = attributes["maximum_damage"]
        self.cooldown = attributes["cooldown"]
        self.accuracy = attributes["accuracy"]
        self.stamina_cost = attributes["stamina_cost"]


class WoodenSword(Weapon):
    """WoodenSword is a basic melee weapon"""

    def __init__(self):
        Weapon.__init__(self, "Wooden Sword")

    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            damage: expected total damage assuming enough stamina
            stamina_cost: expected total stamina cost
        """
        triggers = get_combat_duration() // self.cooldown

        damage = (
            triggers
            * self.accuracy
            * (sum([self.minimum_damage, self.maximum_damage]) / 2)
        )

        stamina_cost = triggers * self.stamina_cost

        metrics = {}
        metrics["damage"] = damage
        metrics["stamina_cost"] = stamina_cost

        return metrics


class Pan(Weapon):
    """Pan is a basic melee weapon scaling with adjacent Food items

    Attributes:
        adjacent_foods: number of adjacent food items
        damage_bonus: how much damage each adjacent food contributes
    """

    def __init__(self, adjacent_foods: int = 1):
        Weapon.__init__(self, "Pan")

        attributes = self.item_data["attributes"]
        self.damage_bonus = attributes["damage_bonus"]
        self.adjacent_foods = adjacent_foods

    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            damage: expected total damage assuming enough stamina
            stamina_cost: expected total stamina cost
        """
        triggers = get_combat_duration() // self.cooldown

        minimum_damage = self.minimum_damage + self.adjacent_foods * self.damage_bonus
        maximum_damage = self.maximum_damage + self.adjacent_foods * self.damage_bonus
        damage = triggers * self.accuracy * (sum([minimum_damage, maximum_damage]) / 2)

        stamina_cost = triggers * self.stamina_cost

        metrics = {}
        metrics["damage"] = damage
        metrics["stamina_cost"] = stamina_cost

        return metrics


class Stone(Weapon):
    """Stone is a ranged weapon which is triggered once per combat unless bag of marbles is present.
       In addition, stone provides armor destruction.

    Attributes:
        armor_destruction: amount of armor removed on hit
        bag_of_marbles: how much damage each adjacent food contributes
    """

    def __init__(self, bag_of_marbles: bool = False):
        Weapon.__init__(self, "Stone")
        self.armor_destruction = self.item_data["attributes"]["armor_destruction"]
        self.bag_of_marbles = bag_of_marbles

    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            damage: expected total damage assuming enough stamina
            armor_destruction: expected total armor destruction
        """
        if self.bag_of_marbles:
            triggers = get_combat_duration() // self.cooldown
        else:
            triggers = 1

        damage = (
            triggers
            * self.accuracy
            * (sum([self.minimum_damage, self.maximum_damage]) / 2)
        )

        armor_destruction = triggers * self.accuracy * self.armor_destruction

        stamina_cost = triggers * self.stamina_cost

        metrics = {}
        metrics["damage"] = damage
        metrics["armor_destruction"] = armor_destruction
        metrics["stamina_cost"] = stamina_cost

        return metrics


class HealingHerbs(Item):
    """HealingHerbs is an item which provides regeneration

    Attributes:
        regeneration: how much passive healing is provided
    """

    def __init__(self):
        Item.__init__(self, "Healing Herbs")

        self.regeneration = self.item_data["attributes"]["regeneration"]

    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            regeneration: how much passive healing is provided
        """

        metrics = {}
        metrics["regeneration"] = self.regeneration

        return metrics


class PocketSand(Item):
    """PocketSand is an item which applies blind to opponent

    Attributes:
        blind: how much blind is applied
    """

    def __init__(self):
        Item.__init__(self, "Pocket Sand")

        self.blind = self.item_data["attributes"]["blind"]

    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            blind: how much blind is applied
        """

        metrics = {}
        metrics["blind"] = self.blind

        return metrics


class WoodenBuckler(Item):
    """WoodenBuckler is an item which has a chance to reduce incoming damage and remove stamina

    Attributes:
        proc_chance: chance to block incoming attack
        damage_absorption: how much damage is absorbed on block
        stamina_removal: how much stamina is removed on block
    """

    def __init__(self):
        Item.__init__(self, "Wooden Buckler")

        self.proc_chance = self.item_data["attributes"]["proc_chance"]
        self.damage_absorption = self.item_data["attributes"]["damage_absorption"]
        self.stamina_removal = self.item_data["attributes"]["stamina_removal"]

    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            damage_absorption: how damage is absorbed
            stamina_damage: how much stamina is removed
        """
        damage_absorption = (
            get_expected_hits() * self.proc_chance * self.damage_absorption
        )
        stamina_damage = get_expected_hits() * self.proc_chance * self.stamina_removal

        metrics = {}
        metrics["damage_absorption"] = damage_absorption
        metrics["stamina_damage"] = stamina_damage

        return metrics


class WalrusTusk(Item):
    """WalrusTusk which provides spikes

    Attributes:
        spikes: how much spikes this item provides
    """

    def __init__(self):
        Item.__init__(self, "Walrus Tusk")

        self.spikes = self.item_data["attributes"]["spikes"]

    def get_metrics(self) -> dict[str, float]:
        """
        Metrics:
            damage: how damage is dealt
        """
        damage = get_expected_hits() * self.spikes

        metrics = {}
        metrics["damage"] = damage

        return metrics
