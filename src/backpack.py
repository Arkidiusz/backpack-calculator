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
        for metrics in self.items.values():
            for metric_name, metric_value in metrics.items():
                match metric_name:
                    case 'stamina':
                        stamina += metric_value
                    case 'healing':
                        healing += metric_value

        self.sps = self.BASE_STAMINA_GENERATION + stamina / get_combat_duration()
        self.hps = healing / get_combat_duration()
