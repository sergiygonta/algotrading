from typing import List
from algorightm.DecisionMaker import DecisionMaker
from historical_data.Quote import Quote, is_red, is_green
from snippets.SnippetConfiguration import PERCENT_OF_GROWTH_OR_FALL_AFTER_SNIPPET, PERCENT_OF_MAXIMUM_ALLOWED_ROLLBACK
from utils.SnippetUtils import create_snippet, SnippetTypes, less_than_interval


class SnippetHybridDataAnalyzer:

    def growing_snippet(quotes: List[Quote], split_point: int, gics: int, company: str):
        if DecisionMaker.should_buy(quotes[0:split_point]) is None:
            return None
        pointer = split_point
        amplitude_of_growth = quotes[split_point].close_price * (1 + PERCENT_OF_GROWTH_OR_FALL_AFTER_SNIPPET / 100)
        amplitude_of_rollback = quotes[split_point].low_price * (1 - PERCENT_OF_MAXIMUM_ALLOWED_ROLLBACK / 100)
        while less_than_interval(quotes[split_point].date, quotes[pointer].date):
            # if graphic goes in the direction where we don't want
            if quotes[pointer].low_price < amplitude_of_rollback and is_red(quotes[pointer]):
                return create_snippet(quotes, split_point, SnippetTypes.hold, gics, company)
            if quotes[pointer].close_price > amplitude_of_growth and is_green(quotes[pointer]):
                return create_snippet(quotes, split_point, SnippetTypes.buy, gics, company)
            pointer += 1
        return create_snippet(quotes, split_point, SnippetTypes.hold, gics, company)

    def falling_snippet(quotes: List[Quote], split_point: int, gics: int, company: str):
        if DecisionMaker.should_sell(quotes[0:split_point]) is None:
            return None
        pointer = split_point
        amplitude_of_fall = quotes[split_point].close_price * (1 - PERCENT_OF_GROWTH_OR_FALL_AFTER_SNIPPET / 100)
        amplitude_of_rollback = quotes[split_point].high_price * (1 + PERCENT_OF_MAXIMUM_ALLOWED_ROLLBACK / 100)
        while less_than_interval(quotes[split_point].date, quotes[pointer].date):
            # if graphic goes in the direction where we don't want
            if quotes[pointer].high_price > amplitude_of_rollback and is_green(quotes[pointer]):
                return create_snippet(quotes, split_point, SnippetTypes.hold, gics, company)
            if quotes[pointer].close_price < amplitude_of_fall and is_red(quotes[pointer]):
                return create_snippet(quotes, split_point, SnippetTypes.sell, gics, company)
            pointer += 1
        return create_snippet(quotes, split_point, SnippetTypes.hold, gics, company)
