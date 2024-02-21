from roboquant.trackers import Tracker


class TensorboardTracker(Tracker):
    """Logs metrics to a Tensorboard compatible file.
    This can be used outside the realm of machine learning, but requires torch to be installed.
    """

    __slots__ = ("items", "ratings", "orders", "writer", "_step")

    def __init__(self, summary_writer):
        self.items: int = 0
        self.ratings: int = 0
        self.orders: int = 0
        self.writer = summary_writer
        self._step = 0

    def log(self, event, account, ratings, orders):
        self.items += len(event.items)
        self.ratings += len(ratings)
        self.orders += len(orders)

        self.writer.add_scalar("Run/items", self.items, self._step)
        self.writer.add_scalar("Run/ratings", self.ratings, self._step)
        self.writer.add_scalar("Run/orders", self.orders, self._step)
        self.writer.add_scalar("Run/equity", account.equity, self._step)
        self._step += 1

    def close(self):
        self.writer.flush()
        self.writer.close()
