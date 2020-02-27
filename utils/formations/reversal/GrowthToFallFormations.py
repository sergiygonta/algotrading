from typing import List

from historical_data.Quote import Quote, lower_shadow, upper_shadow, body_length, is_green, is_red, body_bottom, \
    body_top
from utils.TrendUtils import confirm_trend_reversal


class GrowthToFallFormations:

    # повешенный
    def isHanged(quotes: List[Quote]):
        if len(quotes) < 3:
            return 0
        if is_green(quotes[0]) and is_red(quotes[2]) and body_length(quotes[1]) != 0 and \
                quotes[1].high_price > max(quotes[0].high_price, quotes[2].high_price) and \
                (upper_shadow(quotes[1]) == 0 or lower_shadow(quotes[1]) / upper_shadow(quotes[1]) > 3):
            ratio_shadow_to_body = lower_shadow(quotes[1]) / body_length(quotes[1])
            if ratio_shadow_to_body > 2:
                return confirm_trend_reversal(quotes, ratio_shadow_to_body)
        return 0

    # медвежье поглощение
    def isBearishTakeover(quotes: List[Quote]):
        if len(quotes) >= 2 and is_green(quotes[0]) and is_red(quotes[1]) and \
                quotes[0].open_price < quotes[1].open_price and body_length(quotes[0]) != 0:
            ratio_between_candles = body_length(quotes[1]) / body_length(quotes[0])
            if ratio_between_candles > 1.2:
                return ratio_between_candles
        return 0

    # доджи надгробие
    def isDojiGravestone(quotes: List[Quote]):
        if len(quotes) < 3:
            return 0
        if quotes[1].low_price == body_bottom(quotes[1]) and is_green(quotes[0]) and is_red(quotes[2]) and \
                quotes[1].high_price > body_top(quotes[1]) > max(quotes[0].open_price, quotes[2].close_price) and \
                (body_length == 0 or upper_shadow(quotes[1]) / body_length(quotes[1]) > 3):
            return confirm_trend_reversal(quotes, 1)
        return 0

    # медвежья харами
    def isBearishHarami(quotes: List[Quote]):
        if len(quotes) >= 2 and \
                quotes[0].open_price < quotes[1].close_price < quotes[1].open_price < quotes[0].close_price:
            return confirm_trend_reversal(quotes, 1)
        return 0

    # вечерняя звезда дожи
    def isDojiEveningStar(quotes: List[Quote]):
        if len(quotes) < 3:
            return 0
        if is_green(quotes[0]) and is_red(quotes[2]) and \
                body_bottom(quotes[1]) > max(quotes[0].close_price, quotes[2].open_price) and \
                (body_length(quotes[1]) == 0 or min(lower_shadow(quotes[1]),
                                                    upper_shadow(quotes[1])) / body_length(quotes[1]) > 2):
            return confirm_trend_reversal(quotes, 2)
        return 0

    # брошенный младенец
    def isAbandonedBaby(quotes: List[Quote]):
        if len(quotes) < 3:
            return 0
        if is_green(quotes[0]) and is_red(quotes[2]) and \
                quotes[1].low_price > max(quotes[0].high_price, quotes[2].high_price) and \
                (body_length(quotes[1]) == 0 or min(lower_shadow(quotes[1]),
                                                    upper_shadow(quotes[1])) / body_length(quotes[1]) > 2):
            return confirm_trend_reversal(quotes, 5)
        return 0
