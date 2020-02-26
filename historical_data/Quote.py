from typing import NamedTuple
from datetime import date, datetime

PATH_TO_HISTORICAL_DATA = "../historical_data/SP/"
CSV_HEADER_ROW = 'Date,Open,High,Low,Close,Adj Close,Volume\n'


class Quote(NamedTuple):
    date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    adj_close_price: float
    volume: int


def body_length(quote: Quote):
    return abs(quote.open_price - quote.close_price)


def body_top(quote: Quote):
    return max(quote.open_price, quote.close_price)


def body_bottom(quote: Quote):
    return min(quote.open_price, quote.close_price)


def upper_shadow(quote: Quote):
    return quote.high_price - body_top(quote)


def lower_shadow(quote: Quote):
    return body_bottom(quote) - quote.low_price


def is_green(quote: Quote):
    return quote.open_price < quote.close_price


def is_red(quote: Quote):
    return quote.open_price > quote.close_price
