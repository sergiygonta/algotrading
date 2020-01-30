from typing import List

from Quote import Quote


class Solution:

    def should_buy(quotes: List[Quote]):
        current_day = quotes[len(quotes) - 1]
        middle_local_max_index = -2
        first_local_min_index = -1
        second_local_min_index = -3
        resistance_level = 9999999
        is_growth_tendency = False
        for i in range(len(quotes) - 2, 1, -1):
            if quotes[i].close_price > current_day.close_price or current_day.close_price < current_day.open_price:
                return None
            if quotes[i].high_price > max(quotes[i - 1].high_price, quotes[i + 1].high_price) and quotes[i].open_price < quotes[i].close_price:
                middle_local_max_index = i
            if quotes[i].close_price < min(quotes[i - 1].close_price, quotes[i + 1].close_price) and quotes[i].open_price > quotes[i].close_price:
                second_local_min_index = first_local_min_index
                first_local_min_index = i
            if first_local_min_index < middle_local_max_index < second_local_min_index:
                resistance_level = quotes[middle_local_max_index].high_price
            if quotes[first_local_min_index].close_price < quotes[second_local_min_index].close_price:
                is_growth_tendency = True
            if second_local_min_index > 0:
                if is_growth_tendency and current_day.close_price > resistance_level:
                    return [quotes[middle_local_max_index].date, resistance_level]
                break
        return None

    def should_sell(quotes: List[Quote]):
        current_day = quotes[len(quotes) - 1]
        middle_local_min_index = -2
        first_local_max_index = -1
        second_local_max_index = -3
        support_level = -1
        is_declining_tendency = False
        for i in range(len(quotes) - 2, 1, -1):
            if quotes[i].close_price < current_day.close_price or current_day.close_price > current_day.open_price:
                return None
            if quotes[i].low_price < min(quotes[i - 1].low_price, quotes[i + 1].low_price) and quotes[i].open_price > quotes[i].close_price:
                middle_local_min_index = i
            if quotes[i].close_price > max(quotes[i - 1].close_price, quotes[i + 1].close_price) and quotes[i].open_price < quotes[i].close_price:
                second_local_max_index = first_local_max_index
                first_local_max_index = i
            if first_local_max_index < middle_local_min_index < second_local_max_index:
                support_level = quotes[middle_local_min_index].low_price
            if quotes[first_local_max_index].close_price > quotes[second_local_max_index].close_price:
                is_declining_tendency = True
            if second_local_max_index > 0:
                if is_declining_tendency and current_day.close_price < support_level:
                    return [quotes[middle_local_min_index].date, support_level]
                break
        return None
