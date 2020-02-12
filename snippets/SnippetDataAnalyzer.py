from typing import List
from algorightm.DecisionMaker import DecisionMaker
from historical_data.Quote import Quote
from utils.SnippetUtils import create_3month_snippet, less_that_three_month_interval, SnippetTypes

TEN_PERCENTS = 1.1

class SnippetDataAnalyzer:

    def growing_snippet(quotes: List[Quote], split_point: int):
        if DecisionMaker.should_buy(quotes[0:split_point]) is None:
            return None
        pointer = split_point
        while less_that_three_month_interval(quotes[split_point].date, quotes[pointer].date):
            if TEN_PERCENTS < quotes[pointer].close_price / quotes[split_point].close_price:
                return create_3month_snippet(quotes, split_point, SnippetTypes.buy)
            pointer += 1
        return create_3month_snippet(quotes, split_point, SnippetTypes.hold)

    def falling_snippet(quotes: List[Quote], split_point: int):
        if DecisionMaker.should_sell(quotes[0:split_point]) is None:
            return None
        pointer = split_point
        while less_that_three_month_interval(quotes[split_point].date, quotes[pointer].date):
            if quotes[split_point].close_price / quotes[pointer].close_price > TEN_PERCENTS:
                return create_3month_snippet(quotes, split_point, SnippetTypes.sell)
            pointer += 1
        return create_3month_snippet(quotes, split_point, SnippetTypes.hold)