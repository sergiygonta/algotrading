from typing import List

from historical_data.Quote import Quote, lower_shadow, upper_shadow, body_length, is_green, is_red, body_bottom


class GrowthToFallFormations:

    # повешенный
    def isHanged(quotes: List[Quote]):
        if len(quotes) < 3:
            return False
        if quotes[1].high_price > max(quotes[0].high_price, quotes[2].high_price) and \
                lower_shadow(quotes[1]) / body_length(quotes[1]) > 2 and \
                lower_shadow(quotes[1]) / upper_shadow(quotes[1]) > 3 and \
                (quotes[0].close_price > quotes[2].close_price):
            return True
        return False

    # медвежье поглощение
    def isBearishTakeover(quotes: List[Quote]):
        if len(quotes) == 2 and \
                quotes[0].open_price < quotes[0].close_price and \
                quotes[1].close_price < quotes[1].open_price and \
                quotes[0].open_price < quotes[1].open_price and \
                (quotes[1].close_price - quotes[1].open_price) / (quotes[0].open_price - quotes[0].close_price) > 1.2:
            return True
        return False

    # доджи надгробие
    def isDojiGravestone(quotes: List[Quote]):
        if len(quotes) < 3:
            return False
        body_length = abs(quotes[1].open_price - quotes[1].close_price)
        body_top = max(quotes[1].open_price, quotes[1].close_price)
        body_bottom = min(quotes[1].open_price, quotes[1].close_price)
        if quotes[1].high_price > body_top and \
                quotes[1].low_price == body_bottom and \
                (body_length == 0 or
                 (quotes[1].high_price - body_top) / body_length > 3) and \
                is_green(quotes[0]) and is_red(quotes[2]) and \
                body_top < max(quotes[0].close_price, quotes[2].open_price):
            for i in range[2:6]:
                if quotes[i].close_price < quotes[0].open_price:
                    return True
                if i == len(quotes) - 1:
                    return False
        return False

    # медвежье харами
    def isBearishHarami(quotes: List[Quote]):
        if len(quotes) == 2 and \
                quotes[1].close_price < quotes[1].open_price < quotes[1].close_price < quotes[1].open_price and \
                (quotes[1].close_price - quotes[1].open_price) / (
                quotes[0].open_price - quotes[0].close_price) > 1.2:
            return True
        return False

    # вечерняя звезда дожи
    def isDojiEveningStar(quotes: List[Quote]):
        if len(quotes) < 3:
            return False
        if quotes[0].open_price < quotes[0].close_price and \
                quotes[2].open_price > quotes[2].close_price and \
                body_bottom(quotes[1]) > max(quotes[0].close_price, quotes[2].open_price) and \
                (body_length == 0 or
                 min(quotes[0].close_price - quotes[0].open_price,
                     quotes[1].open_price - quotes[0].close_price) / body_length(quotes[1]) > 3):
            return True
        return False

    # брошенный младенец
    def isAbandonedBaby(quotes: List[Quote]):
        if len(quotes) < 3:
            return False
        if is_green(quotes[0]) and is_red(quotes[2]) and \
                quotes[1].low_price > max(quotes[0].high_price, quotes[2].high_price) and \
                (body_length(quotes[1]) == 0 or
                 min(quotes[0].close_price - quotes[0].open_price,
                     quotes[1].open_price - quotes[0].close_price) / body_length(quotes[1]) > 3):
            return True
        return False
