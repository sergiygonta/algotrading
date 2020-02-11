from typing import List
from algorightm.DecisionMaker import DecisionMaker
from historical_data.Quote import Quote
from snippets.SnippetUtils import create_3month_snippet, less_that_three_month_interval


class SnippetDataAnalyzer:

    def growing_snippet(quotes: List[Quote], split_point: int):
        if DecisionMaker.should_buy(quotes[0:split_point] is not None):
            pointer = split_point
            while less_that_three_month_interval(quotes[pointer].date, quotes[split_point].date):
                if quotes[pointer].close_price / quotes[split_point].close_price > 1.1:
                    create_3month_snippet(quotes, split_point, 'buy')
                    return
                pointer += 1
            create_3month_snippet(quotes, split_point, 'hold')

    def falling_snippet(quotes: List[Quote], split_point: int):
        if DecisionMaker.should_sell(quotes[0:split_point] is not None):
            pointer = split_point
            while less_that_three_month_interval(quotes[pointer].date, quotes[split_point].date):
                if quotes[split_point].close_price / quotes[pointer].close_price > 1.1:
                    create_3month_snippet(quotes, split_point, 'sell')
                    return
                pointer += 1
            create_3month_snippet(quotes, split_point, 'hold')
