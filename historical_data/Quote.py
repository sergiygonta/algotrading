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


def load_market_data_with_np(file_name):
    import numpy as np
    date, open_price, high_price, low_price, close_price, adj_close_price, volume = np.loadtxt(
        file_name,
        delimiter=',',
        usecols=(0, 1, 2, 3, 4, 5, 6),
        unpack=True,
        skiprows=1,
        dtype='datetime64[D], float, float, float, float, float, int')

    out = []

    for date_val, open_val, high_val, low_val, close_val, adj_close_val, vol_val in \
            zip(date, open_price, high_price, low_price, close_price, adj_close_price, volume):
        out.append(Quote(
            date=date_val,
            open_price=open_val,
            high_price=high_val,
            low_price=low_val,
            close_price=close_val,
            adj_close_price=adj_close_val,
            volume=vol_val)
        )

    return out


def simple_load_market_data(file_name):
    import csv
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        out = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[1] == 'null' or row[2] == 'null' or row[3] == 'null' or row[4] == 'null':
                    continue
                out.append(Quote(
                    date=datetime.strptime(row[0], '%Y-%m-%d').date(),
                    open_price=float(row[1]),
                    high_price=float(row[2]),
                    low_price=float(row[3]),
                    close_price=float(row[4]),
                    adj_close_price=float(row[5]),
                    volume=int(row[6]))
                )
                line_count += 1
    return out
