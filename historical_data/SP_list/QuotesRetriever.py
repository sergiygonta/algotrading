from typing import NamedTuple
from datetime import date, datetime
from alpha_vantage.timeseries import TimeSeries


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
    companies_intervals = simple_load_companies("Members.csv")
    print(companies_intervals)
    key = '4ANXB00UDM288O6G'
    ts = TimeSeries(key)
    aapl, meta = ts.get_daily(symbol='AAPL')
    print(aapl)


if __name__ == "__main__":
    main()
