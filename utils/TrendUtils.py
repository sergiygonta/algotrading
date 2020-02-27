from typing import List

from historical_data.Quote import Quote


def confirmation_of_trend_reversal(quotes: List[Quote], force_of_signal: int):
    for i in range[2:6]:
        if quotes[i].close_price < quotes[0].open_price:
            return force_of_signal
        if i == len(quotes) - 1:
            return 0
    return 0
