




from typing import Protocol
from roboquant.account import Account

from roboquant.event import Event 
from roboquant.order import Order


class Tracker(Protocol):
    """Allow for tracking and/or logging of metrics during a run"""

    def log(self, event: Event, account: Account, ratings: dict[str, float], orders: list[Order]):
        """invoked at each step of a run that provides the tracker to calculate metrics and log these"""
        ...
