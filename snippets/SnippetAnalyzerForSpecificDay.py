from typing import Dict

from snippets.SnippetConfiguration import PREDICTION_SIZE_IN_BUSINESS_DAYS, NUMBER_OF_ROWS_IN_SNIPPET_FILE
from utils.SnippetUtils import QUOTES, SPLIT_POINT, CUSTOM_FILE_NAME, create_snippet


def check_snippet(parameters: Dict):
    list_quotes = parameters[QUOTES]
    i = parameters[SPLIT_POINT]
    change_percent = round(list_quotes[i + PREDICTION_SIZE_IN_BUSINESS_DAYS].close_price / list_quotes[i].close_price - 1,2)
    parameters[CUSTOM_FILE_NAME] = str(list_quotes[i - NUMBER_OF_ROWS_IN_SNIPPET_FILE].date) + "_" + str(
        list_quotes[i].date) + "." + str(change_percent)
    return create_snippet(parameters)
