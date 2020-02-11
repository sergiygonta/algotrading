from historical_data.Quote import simple_load_market_data

import os


def main():
    # companies = os.listdir("../historical_data/SP")
    companies = ['FB.csv', 'AAPL.csv', 'AMZN.csv', 'NFLX.csv', 'GOOG.csv']
    companies.sort()
    for company in companies:
        create_snippets_for_company(company)


def create_snippets_for_company(company):
    quotes = simple_load_market_data("../historical_data/SP/" + company)


if __name__ == "__main__":
    main()
