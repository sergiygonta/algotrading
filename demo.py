from datetime import datetime

from Quote import load_market_data_with_np
from Solution import Solution

import plotly.graph_objects as go
import pandas as pd


def main():
    companies = [#'FB',
                 'AAPL'
        #, 'AMZN', 'NFLX', 'GOOG', 'MSFT'
        ]
    for company in companies:
        get_analytics_for_company(company)


def get_analytics_for_company(company):
    print('==========================')
    quotes = load_market_data_with_np('historical_data/10years/' + company + '.csv')

    df = pd.read_csv('historical_data/2years/' + company + '.csv')
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])
    fig.update_layout(
        title=company,
        yaxis_title=company+' Stock'
    )
    lines=[]

    money = 50_000
    stocks = 0
    initial_money = round(money + stocks * quotes[200].open_price, 2)
    print(company + ' initially: date ' + str(quotes[200].date) + ', money ' + str(initial_money) + '$')
    alreadyBought = False
    alreadySold = True
    for i in range(200, len(quotes) - 1, 1):
        begin, resistance_level = Solution.should_buy(quotes[0:i - 1]) or (None, None)
        if not alreadyBought and not(begin is None):
            # print(str(quotes[i].date) + " buy  " + company)
            alreadyBought = True
            alreadySold = False
            stocks = int(money / quotes[i].open_price)
            money -= stocks * quotes[i].open_price
            lines.append([dict(
                    x0=begin, x1=quotes[i].date, y0=resistance_level, y1=resistance_level,
                    line_width=1, name='Resistance line')]
            )
        begin, support_level = Solution.should_sell(quotes[0:i - 1]) or (None, None)
        if not alreadySold and not (begin is None):
            # print(str(quotes[i].date) + " sell " + company)
            alreadySold = True
            alreadyBought = False
            money += stocks * quotes[i].close_price
            stocks = 0
            lines.append([dict(
                    x0=begin, x1=quotes[i].date, y0=support_level, y1=support_level,
                    line_width=1, name='Support line')]
            )
    final_money = round(money + stocks * quotes[len(quotes) - 1].close_price, 2)
    print(company + ' finally:   date ' + str(quotes[len(quotes) - 1].date) + ', money ' + str(final_money) + '$')
    fig.update_layout(shapes=tuple(lines))
    fig.show()


if __name__ == "__main__":
    main()
