from src.items import Item
from src.controller import *

class Backpack:
    """Represents all information in a backpack used to calculate its value

    Attributes:
        items: a mapping of item reference to its metrics
    
    Metrics:
        sps: stamina generation per second
        hps: health generation per second
    """

    BASE_STAMINA_GENERATION = 1

    def __init__(self):        
        self.items = {}
        metrics = self.compute_metrics()
        self._update_metrics(metrics)
    
    def update_item(self, item : Item) -> None:
        """Updates item metrics/adds a new item to items list and recomputes Backpack metrics

        Attributes:
            :item: an item object 
        """

        item_metrics = item.get_metrics()
        self.items[item] = item_metrics 
        
        backpack_metrics = self.compute_metrics()
        self._update_metrics(backpack_metrics)

    
    def compute_metrics(self, item : Item = None) -> dict[str, float]:
        """Computes all metrics in the backpack

        Attributes:
            :item: additional item to those already in the backpack

        :return: a dictionary of metric name to its value
        """
        
        stamina = 0
        healing = 0
        items = self.items
        if item:
            items += {item : item.get_metrics()}
        for metrics in items.values():
            for metric_name, metric_value in metrics.items():
                match metric_name:
                    case 'stamina':
                        stamina += metric_value
                    case 'healing':
                        healing += metric_value

        metrics = {}
        metrics['sps'] = self.BASE_STAMINA_GENERATION + stamina / get_combat_duration()
        metrics['hps'] = healing / get_combat_duration()

        return metrics

    def _update_metrics(self, metrics : dict[str, float]) -> None:
        """ Updates backpack with the given metrics
        Attributes:
            :metrics: dictionary of metric name and its value
        """

        self.sps = metrics['sps']
        self.hps = metrics['hps']
        