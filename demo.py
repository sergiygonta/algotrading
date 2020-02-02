from datetime import datetime

from Quote import load_market_data_with_np
from Solution import Solution

import plotly.graph_objects as go
import pandas as pd


def main():
    companies = ['FB', 'AAPL', 'AMZN', 'NFLX', 'GOOG', 'MSFT']
    for company in companies:
        get_analytics_for_company(company)


def get_analytics_for_company(company):
    print('==========================')
    quotes = load_market_data_with_np('historical_data/10years/' + company + '.csv')
    df = pd.read_csv('historical_data/10years/' + company + '.csv')
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'],
                                         increasing_line_color='white',
                                         decreasing_line_color='black')])
    fig.update_layout(
        title=company,
        yaxis_title=company + ' stocks price',
        xaxis_title="End of green line - buy date. End of red line - sell date.", )

    money = 50_000
    stocks = 0
    initial_money = round(money + stocks * quotes[200].open_price, 2)
    print(company + ' initially: date ' + str(quotes[200].date) + ', money ' + str(initial_money) + '$')
    alreadyBought = False
    alreadySold = True
    price_for_buy = 0
    for i in range(200, len(quotes) - 1, 1):
        begin, resistance_level = Solution.should_buy(quotes[0:i]) or (None, None)
        if not alreadyBought and not (begin is None):
            #print(str(quotes[i].date) + " buy  " + company)
            alreadyBought = True
            alreadySold = False
            stocks = int(money / quotes[i].open_price)
            money -= stocks * quotes[i].open_price
            price_for_buy = quotes[i].open_price
            if resistance_level is not None:
                fig.add_shape(
                    # Line Diagonal
                    go.layout.Shape(
                        type="line",
                        x0=begin,
                        y0=resistance_level,
                        x1=quotes[i].date,
                        y1=resistance_level,
                        line=dict(
                            color="green",
                            width=1,
                        )
                    ))
        begin, support_level = Solution.should_sell(quotes[0:i]) or (None, None)
        if not alreadySold and not (begin is None) and (price_for_buy < quotes[i].close_price):
            alreadySold = True
            alreadyBought = False
            money += stocks * quotes[i].close_price

            #print(str(quotes[i].date) + " sell " + company + " .money=" + str(money))
            stocks = 0
            if support_level is not None:
                fig.add_shape(
                    # Line Diagonal
                    go.layout.Shape(
                        type="line",
                        x0=begin,
                        y0=support_level,
                        x1=quotes[i].date,
                        y1=support_level,
                        line=dict(
                            color="red",
                            width=1,
                        )
                    ))
    final_money = round(money + stocks * quotes[len(quotes) - 1].close_price, 2)
    print(company + ' finally:   date ' + str(quotes[len(quotes) - 1].date) + ', money ' + str(final_money) + '$')
    fig.show()


if __name__ == "__main__":
    main()
