from . import Node
from . import ExitType
import random

available_leverages = [30]
available_tp = [1, 2, 5, 10, 20, 50, 100]
available_sl = [10, 50, 100, 200, 250]

class Member:
    tree:Node = None
    fitness:int = 0
    cumulated_fitness = 0
    success:int = 0
    trades:int = 0
    pips:int = 0

    exit_type:ExitType = ExitType.TP_SL
    tp = 0
    sl = 0
    leverage = 1

    def __init__(self, t:Node):
        self.fitness = 0
        self.cumulated_fitness = 0
        self.tree = t
        self.success = 0
        self.trades = 0
        self.pips = 0
        self.exit_type = random.choice(list(ExitType))
        self.tp = random.choice(available_tp)
        self.sl = random.choice(available_sl)
        self.leverage = random.choice(available_leverages)