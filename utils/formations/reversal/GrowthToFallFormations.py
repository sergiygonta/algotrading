from typing import List

from historical_data.Quote import Quote, lower_shadow, upper_shadow, body_length, is_green, is_red, body_bottom, \
    body_top


# assume that third candle is split point
def is_growth_to_fall(quotes: List[Quote]) -> float:
    if len(quotes) != 6:
        return 0
    bearish_takeover_power = isBearishTakeover(quotes[1:3])
    if bearish_takeover_power != 0:
        return bearish_takeover_power
    if not confirm_growth_to_fall_trend_reversal(quotes):
        return 0
    hanged_power = isHanged(quotes)
    if hanged_power != 0:
        return hanged_power
    doji_dragonfly_power = isDojiGravestone(quotes)
    if doji_dragonfly_power != 0:
        return doji_dragonfly_power
    abandoned_baby_power = isAbandonedBaby(quotes)
    if abandoned_baby_power != 0:
        return abandoned_baby_power
    doji_evening_star_power = isDojiEveningStar(quotes)
    if doji_evening_star_power != 0:
        return doji_evening_star_power
    bearish_harami_power = isBearishHarami(quotes)
    if bearish_harami_power != 0:
        return bearish_harami_power
    return 0


# повешенный
def isHanged(quotes: List[Quote]) -> float:
    if len(quotes) < 3:
        return 0
    if is_green(quotes[0]) and is_red(quotes[2]) and body_length(quotes[1]) != 0 and \
            quotes[1].high_price > max(quotes[0].high_price, quotes[2].high_price) and \
            (upper_shadow(quotes[1]) == 0 or lower_shadow(quotes[1]) / upper_shadow(quotes[1]) > 3):
        ratio_shadow_to_body = lower_shadow(quotes[1]) / body_length(quotes[1])
        if ratio_shadow_to_body > 2:
            return ratio_shadow_to_body
    return 0


# медвежье поглощение
def isBearishTakeover(quotes: List[Quote]) -> float:
    if len(quotes) >= 2 and is_green(quotes[0]) and is_red(quotes[1]) and \
            quotes[0].open_price < quotes[1].open_price and body_length(quotes[0]) != 0:
        ratio_between_candles = body_length(quotes[1]) / body_length(quotes[0])
        if ratio_between_candles > 1.2:
            return ratio_between_candles
    return 0


# доджи надгробие
def isDojiGravestone(quotes: List[Quote]) -> float:
    if len(quotes) < 3:
        return 0
    if quotes[1].low_price == body_bottom(quotes[1]) and is_green(quotes[0]) and is_red(quotes[2]) and \
            quotes[1].high_price > body_top(quotes[1]) > max(quotes[0].open_price, quotes[2].close_price) and \
            (body_length == 0 or upper_shadow(quotes[1]) / body_length(quotes[1]) > 3):
        return 1
    return 0


# медвежья харами
def isBearishHarami(quotes: List[Quote]):
    if len(quotes) >= 2 and \
            quotes[0].open_price < quotes[1].close_price < quotes[1].open_price < quotes[0].close_price:
        return 1
    return 0


# вечерняя звезда дожи
def isDojiEveningStar(quotes: List[Quote]) -> float:
    if len(quotes) < 3:
        return 0
    if is_green(quotes[0]) and is_red(quotes[2]) and \
            body_bottom(quotes[1]) > max(quotes[0].close_price, quotes[2].open_price) and \
            (body_length(quotes[1]) == 0 or min(lower_shadow(quotes[1]),
                                                upper_shadow(quotes[1])) / body_length(quotes[1]) > 2):
        return 2
    return 0


# брошенный младенец
def isAbandonedBaby(quotes: List[Quote]) -> float:
    if len(quotes) < 3:
        return 0
    if is_green(quotes[0]) and is_red(quotes[2]) and \
            quotes[1].low_price > max(quotes[0].high_price, quotes[2].high_price) and \
            (body_length(quotes[1]) == 0 or min(lower_shadow(quotes[1]),
                                                upper_shadow(quotes[1])) / body_length(quotes[1]) > 2):
        return 5
    return 0


def confirm_growth_to_fall_trend_reversal(quotes: List[Quote]) -> bool:
    for i in range[2:6]:
        if quotes[i].close_price < quotes[0].open_price:
            return True
        if i == len(quotes) - 1:
            return False
    return False
