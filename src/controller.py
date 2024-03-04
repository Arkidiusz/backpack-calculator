from .backpack import Backpack

backpack = Backpack()

def request_metrics_update() -> dict[str, float]:
    """Requests backpack to recompute its metrics
        
    :return: a dictionary mapping of metric name to its value
    """
    return backpack.compute_metrics()
