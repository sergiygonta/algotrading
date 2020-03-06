from typing import Dict
from algorightm.DecisionMaker import DecisionMaker
from historical_data.Quote import is_red, is_green
from snippets.SnippetConfiguration import PERCENT_OF_GROWTH_OR_FALL_AFTER_SNIPPET, PERCENT_OF_MAXIMUM_ALLOWED_ROLLBACK, \
    PREDICTION_SIZE_IN_BUSINESS_DAYS
from utils.SnippetUtils import create_snippet, SnippetTypes, QUOTES, SPLIT_POINT, SNIPPET_TYPE

#
from utils.formations.reversal.FallToGrowthFormations import isBullTakeover, is_fall_to_growth
from utils.formations.reversal.GrowthToFallFormations import is_growth_to_fall


def check_snippet(parameters: Dict):
    growing_results = growing_snippet(parameters)
    if growing_results is None or growing_results[SNIPPET_TYPE] != SnippetTypes.buy:
        return falling_snippet(parameters)
    else:
        return growing_results


def growing_snippet(parameters: Dict):
    split_point = parameters[SPLIT_POINT]
    quotes = parameters[QUOTES]
    fall_to_growth_power = is_fall_to_growth(quotes[split_point-2, split_point+4])
    if fall_to_growth_power == 0:
        return None
    amplitude_of_growth = quotes[split_point].close_price * (1 + PERCENT_OF_GROWTH_OR_FALL_AFTER_SNIPPET / 100)
    amplitude_of_rollback = quotes[split_point].low_price * (1 - PERCENT_OF_MAXIMUM_ALLOWED_ROLLBACK / 100)
    for pointer in range(split_point + 1,
                         split_point + PREDICTION_SIZE_IN_BUSINESS_DAYS + 1):
        # if graphic goes in the direction where we don't want
        if quotes[pointer].low_price < amplitude_of_rollback and is_red(quotes[pointer]):
            parameters[SNIPPET_TYPE] = SnippetTypes.hold
            return create_snippet(parameters)
        if quotes[pointer].close_price > amplitude_of_growth and is_green(quotes[pointer]):
            parameters[SNIPPET_TYPE] = SnippetTypes.buy
            return create_snippet(parameters)
        pointer += 1
    parameters[SNIPPET_TYPE] = SnippetTypes.hold
    return create_snippet(parameters)


def falling_snippet(parameters: Dict):
    split_point = parameters[SPLIT_POINT]
    quotes = parameters[QUOTES]
    growth_to_fall_power = is_growth_to_fall(quotes[split_point - 2, split_point + 4])
    if growth_to_fall_power == 0:
        return None
    amplitude_of_fall = quotes[split_point].close_price * (1 - PERCENT_OF_GROWTH_OR_FALL_AFTER_SNIPPET / 100)
    amplitude_of_rollback = quotes[split_point].high_price * (1 + PERCENT_OF_MAXIMUM_ALLOWED_ROLLBACK / 100)
    for pointer in range(split_point + 1,
                         split_point + PREDICTION_SIZE_IN_BUSINESS_DAYS + 1):
        # if graphic goes in the direction where we don't want
        if quotes[pointer].high_price > amplitude_of_rollback and is_green(quotes[pointer]):
            parameters[SNIPPET_TYPE] = SnippetTypes.hold
            return create_snippet(parameters)
        if quotes[pointer].close_price < amplitude_of_fall and is_red(quotes[pointer]):
            parameters[SNIPPET_TYPE] = SnippetTypes.sell
            return create_snippet(parameters)
        pointer += 1
    parameters[SNIPPET_TYPE] = SnippetTypes.hold
    return create_snippet(parameters)
