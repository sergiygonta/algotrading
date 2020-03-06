from typing import List

from historical_data.Quote import Quote, lower_shadow, body_length, upper_shadow, is_green, is_red, body_top, \
    body_bottom


class FallToGrowthFormations:

    # молот
    def isHammer(quotes: List[Quote]) -> float:
        if len(quotes) < 3:
            return 0
        if is_red(quotes[0]) and is_green(quotes[2]) and body_length(quotes[1]) != 0 and \
                quotes[1].low_price < min(quotes[0].low_price, quotes[2].low_price) and \
                lower_shadow(quotes[1]) / upper_shadow(quotes[1]) > 3:
            ratio_shadow_to_body = lower_shadow(quotes[1]) / body_length(quotes[1])
            if ratio_shadow_to_body > 2:
                return confirm_trend_reversal(quotes, ratio_shadow_to_body)
        return 0

    # бычье поглощение
    def isBullTakeover(quotes: List[Quote]) -> float:
        if len(quotes) >= 2 and is_red(quotes[0]) and is_green(quotes[1]) and \
                quotes[0].open_price > quotes[1].open_price and body_length(quotes[0]) != 0:
            ratio_between_candles = body_length(quotes[1]) / body_length(quotes[0])
            if ratio_between_candles > 1.2:
                return ratio_between_candles
        return 0

    # доджи стрекоза
    def isDojiDragonfly(quotes: List[Quote]) -> float:
        if len(quotes) < 3:
            return 0
        if quotes[1].high_price == body_top and is_red(quotes[0]) and is_green(quotes[2]) and \
                quotes[1].low_price < body_bottom(quotes[1]) < min(quotes[0].open_price, quotes[2].close_price) and \
                (body_length == 0 or lower_shadow(quotes[1]) / body_length(quotes[1]) > 3):
            return confirm_trend_reversal(quotes, 1)
        return 0

    # бычья харами
    def isBullHarami(quotes: List[Quote]) -> float:
        if len(quotes) >= 2 and \
                quotes[0].close_price < quotes[1].open_price < quotes[1].close_price < quotes[0].open_price:
            return confirm_trend_reversal(quotes, 1)
        return 0

    # утренняя звезда дожи
    def isDojiMorningStar(quotes: List[Quote]) -> float:
        if len(quotes) < 3:
            return 0
        if is_red(quotes[0]) and is_green(quotes[2]) and \
                body_top(quotes[1]) < min(quotes[0].close_price, quotes[2].open_price) and \
                (body_length(quotes[1]) == 0 or min(lower_shadow(quotes[1]),
                                                    upper_shadow(quotes[1])) / body_length(quotes[1]) > 2):
            return confirm_trend_reversal(quotes, 2)
        return 0

    # брошенный младенец
    def isAbandonedBaby(quotes: List[Quote]) -> float:
        if len(quotes) < 3:
            return 0
        if is_red(quotes[0]) and is_green(quotes[2]) and \
                quotes[1].high_price < min(quotes[0].low_price, quotes[2].low_price) and \
                (body_length(quotes[1]) == 0 or min(lower_shadow(quotes[1]),
                                                    upper_shadow(quotes[1])) / body_length(quotes[1]) > 2):
            return confirm_trend_reversal(quotes, 5)
        return 0


def confirm_trend_reversal(quotes: List[Quote], power_of_signal: float) -> float:
    for i in range[2:6]:
        if quotes[i].close_price > quotes[0].open_price:
            return power_of_signal
        if i == len(quotes) - 1:
            return 0
    return 0
