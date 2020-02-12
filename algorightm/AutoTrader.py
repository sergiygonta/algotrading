from datetime import datetime, date

from historical_data.Quote import simple_load_market_data, PATH_TO_HISTORICAL_DATA
from algorightm.DecisionMaker import DecisionMaker

import plotly.graph_objects as go
import pandas as pd
import os

from utils.GraphicUtils import Colors, draw_candlestick_chart, Line



initial_money = 50_000


def main():
    companies = os.listdir(PATH_TO_HISTORICAL_DATA)
    companies.sort()
    total_earnings = 0
    # for company in companies:
    total_earnings += get_analytics_for_company('AAPL.csv')
    # print('From 2009-04-07 to 2020-01-31 from ' + str(initial_money) + '$ earning ' + str(
    #     round(total_earnings / len(companies), 2)) + '$')


def get_analytics_for_company(company):
    quotes = simple_load_market_data(PATH_TO_HISTORICAL_DATA + company)
    if len(quotes) < 101:
        return initial_money
    lines = []
    money = initial_money
    stocks = 0
    alreadyBought = False
    alreadySold = True
    price_for_buy = 0
    for i in range(100, len(quotes) - 1, 1):
        begin, resistance_level = DecisionMaker.should_buy(quotes[0:i]) or (None, None)
        if not alreadyBought and not (begin is None):
            # print(str(quotes[i].date) + " buy  " + company)
            alreadyBought = True
            alreadySold = False
            stocks = int(money / quotes[i].open_price)
            money -= stocks * quotes[i].open_price
            price_for_buy = quotes[i].open_price
            if resistance_level is not None:
                lines.append(Line(begin,resistance_level,quotes[i].date,resistance_level,Colors.green.name))
        begin, support_level = DecisionMaker.should_sell(quotes[0:i]) or (None, None)
        if not alreadySold and not (begin is None) and (price_for_buy < quotes[i].close_price):
            alreadySold = True
            alreadyBought = False
            money += stocks * quotes[i].close_price

            # print(str(quotes[i].date) + " sell " + company + " .money=" + str(money))
            stocks = 0
            if support_level is not None:
                lines.append(Line(begin, support_level, quotes[i].date, support_level, Colors.red.name))
    final_money = round(money + stocks * quotes[len(quotes) - 1].close_price, 2)
    print('{0:<9} from '.format(company) + str(quotes[100].date) + ' and 50000$ to ' +
          str(quotes[len(quotes) - 1].date) + ' and ' + str(final_money) + '$')
    draw_candlestick_chart(PATH_TO_HISTORICAL_DATA, company, lines, "End of green line - buy date. End of red line - sell date.")
    return final_money - initial_money


if __name__ == "__main__":
    main()
