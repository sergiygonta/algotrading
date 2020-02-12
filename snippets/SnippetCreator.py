from datetime import timedelta

from historical_data.Quote import simple_load_market_data, PATH_TO_HISTORICAL_DATA
from utils.GraphicUtils import draw_candlestick_chart, Colors, Line
from utils.SnippetUtils import analyze_from, analyze_to, less_that_three_month_interval, clear_snippets_directories
from snippets.SnippetDataAnalyzer import SnippetDataAnalyzer

def main():
    # companies = os.listdir("../historical_data/SP")
    companies = ['FB.csv'
       # , 'AAPL.csv', 'AMZN.csv', 'NFLX.csv', 'GOOG.csv'
                 ]
    companies.sort()
    for company in companies:
        create_snippets_for_company(company)


def create_snippets_for_company(company):
    clear_snippets_directories()
    lines = []
    quotes = simple_load_market_data(PATH_TO_HISTORICAL_DATA + company)
    if not quotes or less_that_three_month_interval(quotes[0].date, quotes[len(quotes) - 1].date):
        return
    for i in range(analyze_from(quotes), analyze_to(quotes), 1):
        left_border, right_border, snippet_type = SnippetDataAnalyzer.growing_snippet(quotes, i) or (None, None, None)
        if left_border is not None:
            lines.append(Line(quotes[left_border].date, quotes[left_border].close_price, quotes[right_border].date,
                              quotes[right_border].close_price, Colors(snippet_type.value).name))
        left_border, right_border, snippet_type = SnippetDataAnalyzer.falling_snippet(quotes, i) or (None, None, None)
        if left_border is not None:
            lines.append(Line(quotes[left_border].date, quotes[left_border].close_price, quotes[right_border].date,
                              quotes[right_border].close_price, Colors(snippet_type.value).name))
    draw_candlestick_chart(PATH_TO_HISTORICAL_DATA, company, lines, "After green = buy, after red = sell, after blue = hold")

if __name__ == "__main__":
    main()
