from datetime import timedelta

from historical_data.Quote import simple_load_market_data
from snippets.SnippetUtils import analyze_from, analyze_to, less_that_three_month_interval
from snippets.SnippetDataAnalyzer import SnippetDataAnalyzer


def main():
    # companies = os.listdir("../historical_data/SP")
    companies = ['FB.csv', 'AAPL.csv', 'AMZN.csv', 'NFLX.csv', 'GOOG.csv']
    companies.sort()
    for company in companies:
        create_snippets_for_company(company)


def create_snippets_for_company(company):
    quotes = simple_load_market_data("../historical_data/SP/" + company)
    if not quotes or less_that_three_month_interval(quotes[len(quotes) - 1].date, quotes[0].date):
        return
    for i in range(analyze_from(quotes), analyze_to(quotes), 1):
        SnippetDataAnalyzer.growing_snippet(quotes, i)
        SnippetDataAnalyzer.falling_snippet(quotes, i)


if __name__ == "__main__":
    main()
