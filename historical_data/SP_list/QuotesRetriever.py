from typing import NamedTuple
from datetime import date, datetime
from alpha_vantage.timeseries import TimeSeries
import pandas as pd


class CompanyInterval(NamedTuple):
    company: str
    date_from: date
    date_to: date


def simple_load_companies(file_name):
    import csv
    out = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        out = []
        for row in csv_reader:
            if line_count == 0:
                line_count = 1
                continue
            else:
                out.append(CompanyInterval(
                    company=str(row[0]),
                    date_from=datetime.strptime(row[1], '%Y-%m-%d').date(),
                    date_to=datetime.strptime(row[2], '%Y-%m-%d').date())
                )
                line_count += 1
    return out


def main():
    key = '4ANXB00UDM288O6G'
    ts = TimeSeries(key)
    # [0:1] is just for test purpose, to do not fetch all the companies at once
    companies_intervals = simple_load_companies("Members.csv")[0:1]
    for company_interval in companies_intervals:
        print('Date,Open,High,Low,Close,Volume')
        quotes, meta = ts.get_daily(symbol=company_interval.company, outputsize='full')
        for date in pd.date_range(company_interval.date_from, company_interval.date_to).strftime("%Y-%m-%d").tolist():
            if date in quotes:
                print(date +','+ str(quotes[date]['1. open'])+','+ str(quotes[date]['1. open'])+','+ str(quotes[date]['2. high'])+','
                      + str(quotes[date]['3. low'])+','+ str(quotes[date]['4. close'])+','+ str(quotes[date]['5. volume']))


if __name__ == "__main__":
    main()
