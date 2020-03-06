from typing import List

from historical_data.Quote import Quote, lower_shadow, body_length, upper_shadow, is_green, is_red, body_top, \
    body_bottom


# assume that third candle is split point
def is_fall_to_growth(quotes: List[Quote]) -> float:
    if len(quotes) != 6:
        return 0
    bull_takeover_power = isBullTakeover(quotes[1:3])
    if bull_takeover_power != 0:
        return bull_takeover_power
    if not confirm_fall_to_growth_trend_reversal:
        return False
    hammer_power = isHammer(quotes)
    if hammer_power != 0:
        return hammer_power
    doji_dragonfly_power = isDojiDragonfly(quotes)
    if doji_dragonfly_power != 0:
        return doji_dragonfly_power
    abandoned_baby_power = isAbandonedBaby(quotes)
    if abandoned_baby_power != 0:
        return abandoned_baby_power
    doji_morning_star_power = isDojiMorningStar(quotes)
    if doji_morning_star_power != 0:
        return doji_morning_star_power
    bull_harami_power = isBullHarami(quotes)
    if bull_harami_power != 0:
        return bull_harami_power
    return 0


# молот
def isHammer(quotes: List[Quote]) -> float:
    if len(quotes) < 3:
        return 0
    if is_red(quotes[0]) and is_green(quotes[2]) and body_length(quotes[1]) != 0 and \
            quotes[1].low_price < min(quotes[0].low_price, quotes[2].low_price) and \
            (upper_shadow(quotes[1]) == 0 or lower_shadow(quotes[1]) / upper_shadow(quotes[1]) > 3):
        ratio_shadow_to_body = lower_shadow(quotes[1]) / body_length(quotes[1])
        if ratio_shadow_to_body > 2:
            return ratio_shadow_to_body
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
        return confirm_fall_to_growth_trend_reversal(quotes, 1)
    return 0


# бычья харами
def isBullHarami(quotes: List[Quote]) -> float:
    if len(quotes) >= 2 and \
            quotes[0].close_price < quotes[1].open_price < quotes[1].close_price < quotes[0].open_price:
        return 1
    return 0


# утренняя звезда дожи
def isDojiMorningStar(quotes: List[Quote]) -> float:
    if len(quotes) < 3:
        return 0
    if is_red(quotes[0]) and is_green(quotes[2]) and \
            body_top(quotes[1]) < min(quotes[0].close_price, quotes[2].open_price) and \
            (body_length(quotes[1]) == 0 or min(lower_shadow(quotes[1]),
                                                upper_shadow(quotes[1])) / body_length(quotes[1]) > 2):
        return 2
    return 0


# брошенный младенец
def isAbandonedBaby(quotes: List[Quote]) -> float:
    if len(quotes) < 3:
        return 0
    if is_red(quotes[0]) and is_green(quotes[2]) and \
            quotes[1].high_price < min(quotes[0].low_price, quotes[2].low_price) and \
            (body_length(quotes[1]) == 0 or min(lower_shadow(quotes[1]),
                                                upper_shadow(quotes[1])) / body_length(quotes[1]) > 2):
        return 5
    return 0


def confirm_fall_to_growth_trend_reversal(quotes: List[Quote]) -> bool:
    for i in range(2, 6):
        if quotes[i].close_price > quotes[0].open_price:
            return True
        if i == len(quotes) - 1:
            return False
    return False
