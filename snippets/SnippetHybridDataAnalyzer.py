from typing import List
from algorightm.DecisionMaker import DecisionMaker
from historical_data.Quote import Quote
from snippets.SnippetConfiguration import PERCENTAGE_OF_GROWTH_OR_FALL_AFTER_SNIPPET
from utils.SnippetUtils import create_snippet, SnippetTypes, less_than_interval

AMPLITUDE_OF_CHANGE = 1 + PERCENTAGE_OF_GROWTH_OR_FALL_AFTER_SNIPPET / 100


class SnippetHybridDataAnalyzer:

    def growing_snippet(quotes: List[Quote], split_point: int, gics: int, company: str):
        if DecisionMaker.should_buy(quotes[0:split_point]) is None:
            return None
        pointer = split_point
        while less_than_interval(quotes[split_point].date, quotes[pointer].date):
            if AMPLITUDE_OF_CHANGE < quotes[pointer].close_price / quotes[split_point].close_price:
                return create_snippet(quotes, split_point, SnippetTypes.buy, gics, company)
            pointer += 1
        return create_snippet(quotes, split_point, SnippetTypes.hold, gics, company)

    def falling_snippet(quotes: List[Quote], split_point: int, gics: int, company: str):
        if DecisionMaker.should_sell(quotes[0:split_point]) is None:
            return None
        pointer = split_point
        while less_than_interval(quotes[split_point].date, quotes[pointer].date):
            if quotes[split_point].close_price / quotes[pointer].close_price > AMPLITUDE_OF_CHANGE:
                return create_snippet(quotes, split_point, SnippetTypes.sell, gics, company)
            pointer += 1
        return create_snippet(quotes, split_point, SnippetTypes.hold, gics, company)