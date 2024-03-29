from .items import Item
import src.config as config


class Backpack:
    """Represents all information in a backpack used to calculate its value

    Attributes:
        items: a mapping of item reference to its metrics

    Metrics:
        sps: stamina generation per second
        hps: health generation per second
    """

    BASE_STAMINA_GENERATION = 1
    BASE_STAMINA = 5

    def __init__(self):
        self.items = {}
        self.metrics = self.compute_metrics()
        self._update_metrics(self.metrics)

    def update_item(self, item: Item) -> None:
        """Updates item metrics/adds a new item to items list and recomputes Backpack metrics

        Args:
            item (Item): an item object
        """

        item_metrics = item.get_metrics()
        self.items[item] = item_metrics

        backpack_metrics = self.compute_metrics()
        self._update_metrics(backpack_metrics)

    def update_items(self) -> None:
        """Updates metrics of all items"""

        for item in self.items:
            metrics = item.get_metrics()
            self.items[item] = metrics
            self.metrics[item] = metrics

    def compute_metrics(self, item: Item = None) -> dict[str, float]:
        """Computes all metrics in the backpack

        Args:
            item (Item, optional): additional item to those already in the backpack. Defaults to None.

        Returns:
            dict[str, float]: a dictionary of metric name to its value
        """

        stamina = self.BASE_STAMINA
        healing = 0
        stamina_cost = 0
        damage = 0
        armor = 0
        vampirism_removal = 0
        armor_destruction = 0
        regeneration = 0
        blind = 0
        damage_absorption = 0
        stamina_damage = 0
        items = self.items
        if item:
            items += {item: item.get_metrics()}
        for metrics in items.values():
            for metric_name, metric_value in metrics.items():
                match metric_name:
                    case "stamina":
                        stamina += metric_value
                    case "healing":
                        healing += metric_value
                    case "stamina_cost":
                        stamina_cost += metric_value
                    case "damage":
                        damage += metric_value
                    case "armor":
                        armor += metric_value
                    case "vampirism_removal":
                        vampirism_removal += metric_value
                    case "armor_destruction":
                        armor_destruction += metric_value
                    case "regeneration":
                        regeneration += metric_value
                    case "blind":
                        blind += metric_value
                    case "damage_absorption":
                        damage_absorption += metric_value
                    case "stamina_damage":
                        stamina_damage += metric_value

        metrics = {}

        metrics["armor"] = armor

        metrics["vampirism_removal"] = vampirism_removal

        regeneration_triggers = config.combat_duration // 2
        healing += regeneration_triggers * regeneration
        metrics["hps"] = healing / config.combat_duration

        metrics["sps"] = (
            self.BASE_STAMINA_GENERATION
            + (stamina - stamina_cost) / config.combat_duration
        )

        dps = damage / config.combat_duration
        if stamina_cost > stamina:
            dps = dps * (stamina / stamina_cost)
        metrics["dps"] = dps

        metrics["armor_destruction"] = armor_destruction

        metrics["blind"] = blind

        metrics["damage_absorption"] = damage_absorption

        metrics["stamina_damage"] = stamina_damage

        # round metrics
        for name, value in metrics.items():
            metrics[name] = round(value, 2)

        return metrics

    def _update_metrics(self, metrics: dict[str, float]) -> None:
        """Updates backpack with the given metrics

        Args:
            metrics (dict[str, float]): dictionary of metric name and its value
        """

        self.sps = metrics["sps"]
        self.hps = metrics["hps"]
