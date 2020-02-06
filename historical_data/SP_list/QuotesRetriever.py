from typing import NamedTuple
from datetime import date, datetime

import urllib.request


from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import os, shutil
import csv
import time

QUOTES_FOLDER_PATH = '../SP/'


class CompanyInterval(NamedTuple):
    name: str
    date_from: date
    date_to: date


def clear_quotes_directory():
    for filename in os.listdir(QUOTES_FOLDER_PATH):
        file_path = os.path.join(QUOTES_FOLDER_PATH, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


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
                    name=str(row[0]),
                    date_from=datetime.strptime(row[1], '%Y-%m-%d').date(),
                    date_to=datetime.strptime(row[2], '%Y-%m-%d').date())
                )
                line_count += 1
    return out


def alpha_vantage_retriever():
    # clean if needed
    # clear_quotes_directory()
    key = '4ANXB00UDM288O6G'
    ts = TimeSeries(key)
    # today 0 - 400, tomorrow from 400 to end
    companies = simple_load_companies("Members.csv")[506:725]  # if not premium alphavantage - only 500 calls per day
    counter = 0
    for company in companies:
        counter += 1
        with open(QUOTES_FOLDER_PATH + company.name + '.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_NONE)
            csv_writer.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
            quotes, meta = ts.get_daily(symbol=company.name, outputsize='full')
            for date in pd.date_range(company.date_from, company.date_to).strftime("%Y-%m-%d").tolist():
                if date in quotes:
                    csv_writer.writerow(
                        [date, str(quotes[date]['1. open']), str(quotes[date]['1. open']), str(quotes[date]['2. high']),
                         str(quotes[date]['3. low']), str(quotes[date]['4. close']),'0.0', str(quotes[date]['5. volume'])])
        if counter % 5 == 0:
            time.sleep(60)  # if not premium alphavantage - only 5 request per minute

def macro_trends_retriever():
    companies = simple_load_companies("Members.csv")[0:1]
    for company in companies:
        with open(QUOTES_FOLDER_PATH + company.name + '.csv', 'w') as csvfile:
            csvfile.write('Date,Open,High,Low,Close,Volume\n')
            target_url = 'http://download.macrotrends.net/assets/php/stock_data_export.php?t='+company.name.lower()
            counter = 0
            for line in urllib.request.urlopen(target_url):
                counter += 1
                if counter < 16:
                    continue
                else:
                    csvfile.write(line.decode('utf-8').rstrip()+'\n')


if __name__ == "__main__":
    #alpha_vantage_retriever()
    macro_trends_retriever()

