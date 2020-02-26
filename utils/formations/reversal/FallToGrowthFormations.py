from typing import List

from historical_data.Quote import Quote, lower_shadow, body_length, upper_shadow, is_green, is_red, body_top, \
    body_bottom


class FallToGrowthFormations:

    # молот
    def isHammer(quotes: List[Quote]):
        if len(quotes) < 3:
            return False
        if quotes[1].low_price < min(quotes[0].low_price, quotes[2].low_price) and \
                lower_shadow(quotes[1]) / body_length(quotes[1]) > 2 and \
                lower_shadow(quotes[1]) / upper_shadow(quotes[1]) > 3 and \
                quotes[0].close_price < quotes[2].close_price:
            return True
        return False

    # бычье поглощение
    def isBullTakeover(quotes: List[Quote]):
        if len(quotes) == 2 and \
                is_red(quotes[0]) and is_green(quotes[1]) and \
                quotes[0].open_price > quotes[1].open_price and \
                body_length(quotes[1]) / body_length(quotes[0]) > 1.2:
            return True
        return False

    # доджи стрекоза
    def isDojiDragonfly(quotes: List[Quote]):
        if len(quotes) < 3:
            return False
        if quotes[1].high_price == body_top and \
                quotes[1].low_price < body_bottom(quotes[1]) and \
                (body_length == 0 or lower_shadow(quotes[1]) / body_length(quotes[1]) > 3) and \
                is_red(quotes[0]) and is_green(quotes[2]) and \
                body_bottom(quotes[1]) < min(quotes[0].close_price, quotes[2].open_price):
            for i in range[2:6]:
                if quotes[i].close_price > quotes[0].open_price:
                    return True
                if i == len(quotes) - 1:
                    return False
        return False

    # бычье харами
    def isBullHarami(quotes: List[Quote]):
        if len(quotes) == 2 and \
                quotes[1].open_price < quotes[0].close_price < quotes[0].open_price < quotes[1].close_price and \
                body_length(quotes[1]) / body_length(quotes[0]) > 1.2:
            return True
        return False

    # утренняя звезда дожи
    def isDojiMorningStar(quotes: List[Quote]):
        if len(quotes) < 3:
            return False
        if is_red(quotes[0]) and is_green(quotes[2]) and \
                body_top(quotes[1]) < min(quotes[0].close_price, quotes[2].open_price) and \
                (body_length(quotes[1]) == 0 or
                 min(quotes[0].open_price - quotes[0].close_price,
                     quotes[1].close_price - quotes[0].open_price) / body_length(quotes[1]) > 3):
            return True
        return False

    # брошенный младенец
    def isAbandonedBaby(quotes: List[Quote]):
        if len(quotes) < 3:
            return False
        if is_red(quotes[0]) and is_green(quotes[2]) and \
                quotes[1].high_price < min(quotes[0].low_price, quotes[2].low_price) and \
                (body_length(quotes[1]) == 0 or
                 min(quotes[0].open_price - quotes[0].close_price,
                     quotes[1].close_price - quotes[0].open_price) / body_length(quotes[1]) > 3):
            return True
        return False
