import bisect
import collections
from datetime import timedelta
from enum import Enum

PriceEvent = collections.namedtuple("PriceEvent", ["timestamp", "price"])


class StockSignal(Enum):
    buy = 1
    neutral = 0
    sell = -1

class Stock:
    LONG_TERM_TIMESPAN = 10
    SHORT_TERM_TIMESPAN = 5

    def __init__(self, symbol):
        self.symbol = symbol
        self.price_history = []

    @property
    def price(self):
        return self.price_history[-1].price \
            if self.price_history else None

    def update(self, timestamp, price):
        if price < 0:
            raise ValueError("price should not be negative")
        bisect.insort_left(self.price_history, PriceEvent(timestamp, price))

    def is_increasing_trend(self):
        return self.price_history[-3].price < \
            self.price_history[-2].price < self.price_history[-1].price

    def _get_closing_price_list(self, on_date, num_days):
        closing_price_list = []
        for i in range(num_days):
            chk = on_date.date() - timedelta(i)
            for price_event in reversed(self.series):
                if price_event.timestamp.date() > chk:
                    pass
                if price_event.timestamp.date() == chk:
                    closing_price_list.insert(0, price_event)
                    break
                if price_event.timestamp.date() < chk:
                    closing_price_list.insert(0, price_event)
                    break

    def get_crossover_signal(self, on_date):
        closing_price_list = []
        NUM_DAYS =self.LONG_TERM_TIMESPAN + 1
        for i in range(11):
            chk = on_date.date() - timedelta(i)
            for price_event in reversed(self.price_history):
                if price_event.timestamp.date() > chk:
                    pass
                if price_event.timestamp.date() == chk:
                    cpl.insert(0, price_event)
                    break
                if price_event.timestamp.date() < chk:
                    cpl.insert(0, price_event)
                    break

        # Return NEUTRAL signal
        if len(closing_price_list) < 11:
            return 0

        # BUY signal
        if sum([update.price for update in cpl[-11:-1]])/10 \
                > sum([update.price for update in cpl[-6:-1]])/5 \
            and sum([update.price for update in cpl[-10:]])/10 \
                < sum([update.price for update in cpl[-5:]])/5:
                    return 1

        # BUY signal
        if sum([update.price for update in cpl[-11:-1]])/10 \
                < sum([update.price for update in cpl[-6:-1]])/5 \
            and sum([update.price for update in cpl[-10:]])/10 \
                > sum([update.price for update in cpl[-5:]])/5:
                    return -1

        # NEUTRAL signal
        return StockSignal.neutral
