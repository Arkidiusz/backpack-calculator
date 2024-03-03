from .backpack import Backpack

backpack = Backpack()

def update_metrics():
    return backpack.compute_metrics()
