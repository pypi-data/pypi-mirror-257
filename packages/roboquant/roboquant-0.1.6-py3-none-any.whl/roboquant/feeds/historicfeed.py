from datetime import datetime
from .feed import Feed
from roboquant.event import Event, PriceItem
from roboquant.timeframe import Timeframe
from typing import List
from abc import ABC
from .eventchannel import EventChannel
from itertools import chain

class HistoricFeed(Feed, ABC):
    """Base class for other feeds that want to produce historic price-items.
    """
    
    def __init__(self):
        super().__init__()
        self._data = {}
        self._modified = False
        self._symbols = []

    def _add_item(self, time: datetime, item: PriceItem):
        """Add an price-item at a moment in time to this feed"""

        self._modified = True

        if time not in self._data:
            self._data[time] = [item] 
        else:
            items = self._data[time]
            items.append(item)

    @property
    def symbols(self):
        self.__update()
        return self._symbols

    def timeline(self) -> List[datetime]:
        self.__update()
        return list(self._data.keys())
    
    def timeframe(self):
        tl = self.timeline()
        if len(tl) == 0:
            return Timeframe.empty()
        else:
            return Timeframe(tl[0], tl[-1], inclusive=True)

    def __update(self):
        if self._modified:
            self._data = dict(sorted(self._data.items()))
            price_items = chain.from_iterable(self._data.values())
            self._symbols = list({item.symbol for item in price_items})
            self._modified = False

    def play(self, channel: EventChannel):
        self.__update()
        for k,v in self._data.items():
            evt = Event(k, v)
            channel.put(evt)