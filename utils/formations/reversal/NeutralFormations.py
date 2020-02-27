from typing import List

from historical_data.Quote import Quote, upper_shadow, lower_shadow, body_bottom, body_length, body_top


class NeutralFormations:
    # длинноногий доджи
    def isLeggyDoji(quotes: List[Quote]):
        if len(quotes) >= 1 and quotes[0].high_price > body_top(quotes[0]) and \
                quotes[0].low_price < body_bottom(quotes[0]) and \
                (body_length(quotes[0]) == 0 or
                 (min(upper_shadow(quotes[0]), lower_shadow(quotes[0])) / body_length > 3)):
            return True
        return False

    # доджи 4 цен
    def isDoji4prices(quotes: List[Quote]):
        return len(quotes) >= 1 and quotes[0].low_price == quotes[0].open_price == \
               quotes[0].close_price == quotes[0].high_price