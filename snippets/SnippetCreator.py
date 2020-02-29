import multiprocessing
import os
from multiprocessing.pool import ThreadPool

from historical_data.Quote import PATH_TO_HISTORICAL_DATA
from historical_data.SP_list.GicsSectors import get_gics_code_by_company
from snippets.SnippetConfiguration import NUMBER_OF_ROWS_IN_SNIPPET_FILE
from snippets.SnippetDataAnalyzer import SnippetDataAnalyzer
from snippets.SnippetHybridDataAnalyzer import SnippetHybridDataAnalyzer
from utils.FileUtils import simple_load_market_data
from utils.GraphicUtils import draw_candlestick_chart, Colors, Line
from utils.SnippetUtils import clear_snippets_directory, less_than_interval, analyze_to, SNIPPET_X_AXIS_TEXT


# please note: configuration is in SnippetConfiguration.py

def main():
    clear_snippets_directory()
    companies = os.listdir("../historical_data/SP")
    companies.sort()
    pool = ThreadPool(multiprocessing.cpu_count())
    pool.map(create_snippets_for_company, companies)


def create_snippets_for_company(company: str):
    lines = []
    quotes = simple_load_market_data(PATH_TO_HISTORICAL_DATA + company)
    comp_name = company[0:len(company) - 4]
    gics = get_gics_code_by_company(comp_name)
    if not quotes or less_than_interval(quotes[0].date, quotes[len(quotes) - 1].date):
        return
    for i in range(NUMBER_OF_ROWS_IN_SNIPPET_FILE, analyze_to(quotes), 1):
        left_border, right_border, snippet_type = SnippetDataAnalyzer.growing_snippet(quotes, i, gics, comp_name) or (
            None, None, None)
        if left_border is not None:
            lines.append(Line(quotes[left_border].date, quotes[left_border].close_price, quotes[right_border].date,
                              quotes[right_border].close_price, Colors(snippet_type.value).name))
        left_border, right_border, snippet_type = SnippetDataAnalyzer.falling_snippet(quotes, i, gics, comp_name) or (
            None, None, None)
        if left_border is not None:
            lines.append(Line(quotes[left_border].date, quotes[left_border].close_price, quotes[right_border].date,
                              quotes[right_border].close_price, Colors(snippet_type.value).name))
    # draw_candlestick_chart(PATH_TO_HISTORICAL_DATA, company, lines, SNIPPET_X_AXIS_TEXT)


if __name__ == "__main__":
    main()
