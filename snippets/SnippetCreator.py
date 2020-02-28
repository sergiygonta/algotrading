import os

from historical_data.Quote import PATH_TO_HISTORICAL_DATA
from historical_data.SP_list.GicsSectors import get_gics_code_by_company
from utils.FileUtils import simple_load_market_data
from utils.GraphicUtils import draw_candlestick_chart, Colors, Line
from utils.SnippetUtils import analyze_from, analyze_to, less_that_three_month_interval, clear_snippets_directories
from snippets.SnippetDataAnalyzer import SnippetDataAnalyzer

PERCENTAGE_OF_GROWTH_OR_FALL_AFTER_SNIPPET = 10


def main():
    clear_snippets_directories()
    companies = os.listdir("../historical_data/SP")
    companies.sort()
    for company in companies:
        create_snippets_for_company(company[0:len(company) - 4])


def create_snippets_for_company(company):
    lines = []
    quotes = simple_load_market_data(PATH_TO_HISTORICAL_DATA + company)
    gics = get_gics_code_by_company(company)
    if not quotes or less_that_three_month_interval(quotes[0].date, quotes[len(quotes) - 1].date):
        return
    for i in range(analyze_from(quotes), analyze_to(quotes), 1):
        left_border, right_border, snippet_type = SnippetDataAnalyzer.growing_snippet(quotes, i, gics) or (
            None, None, None)
        if left_border is not None:
            lines.append(Line(quotes[left_border].date, quotes[left_border].close_price, quotes[right_border].date,
                              quotes[right_border].close_price, Colors(snippet_type.value).name))
        left_border, right_border, snippet_type = SnippetDataAnalyzer.falling_snippet(quotes, i, gics) or (
            None, None, None)
        if left_border is not None:
            lines.append(Line(quotes[left_border].date, quotes[left_border].close_price, quotes[right_border].date,
                              quotes[right_border].close_price, Colors(snippet_type.value).name))
    # draw_candlestick_chart(PATH_TO_HISTORICAL_DATA, company, lines, "After green = buy, after red = sell, after blue = hold")


if __name__ == "__main__":
    main()
