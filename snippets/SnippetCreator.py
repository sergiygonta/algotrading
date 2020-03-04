import multiprocessing
import os
from multiprocessing.pool import ThreadPool

from historical_data.Quote import PATH_TO_HISTORICAL_DATA
from historical_data.SP_list.GicsSectors import get_gics_code_by_company
from snippets import SnippetHybridDataAnalyzer, SnippetDataAnalyzer, SnippetAnalyzerForSpecificDay
from snippets.SnippetConfiguration import NUMBER_OF_ROWS_IN_SNIPPET_FILE, PREDICTION_SIZE_IN_BUSINESS_DAYS
from utils.FileUtils import simple_load_market_data
from utils.GraphicUtils import draw_candlestick_chart, Colors, Line
from utils.SnippetUtils import clear_snippets_directory, SNIPPET_X_AXIS_TEXT, GICS, SPLIT_POINT, QUOTES, \
    COMPANY, SNIPPET_TYPE


def main():
    clear_snippets_directory()
    # companies = os.listdir("../historical_data/SP")
    companies = ['FB.csv']
    companies.sort()
    pool = ThreadPool(multiprocessing.cpu_count())
    pool.map(create_snippets_for_company, companies)


def create_snippets_for_company(company: str):
    lines = []
    quotes = simple_load_market_data(PATH_TO_HISTORICAL_DATA + company)
    comp_name = company[0:len(company) - 4]
    parameters = {QUOTES: quotes, GICS: get_gics_code_by_company(comp_name), COMPANY: comp_name}
    for i in range(NUMBER_OF_ROWS_IN_SNIPPET_FILE, len(quotes) - PREDICTION_SIZE_IN_BUSINESS_DAYS):
        parameters[SPLIT_POINT] = i
        return_parameters = SnippetAnalyzerForSpecificDay.check_snippet(parameters)
    #     if return_parameters is not None and SNIPPET_TYPE in return_parameters.keys():
    #         left_border_of_snippet = i - NUMBER_OF_ROWS_IN_SNIPPET_FILE
    #         lines.append(
    #             Line(quotes[left_border_of_snippet].date, quotes[left_border_of_snippet].close_price, quotes[i].date,
    #                  quotes[i].close_price, Colors(return_parameters[SNIPPET_TYPE].value).name))
    # draw_candlestick_chart(company, lines, SNIPPET_X_AXIS_TEXT)


if __name__ == "__main__":
    main()
