from typing import List

from historical_data.Quote import Quote


def confirm_trend_reversal(quotes: List[Quote], power_of_signal: float) -> float:
    for i in range[2:6]:
        if quotes[i].close_price < quotes[0].open_price:
            return power_of_signal
        if i == len(quotes) - 1:
            return 0
    return 0
