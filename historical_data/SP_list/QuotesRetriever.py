from typing import NamedTuple
from datetime import date, datetime

import urllib.request
import os, shutil

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

def macro_trends_retriever():
    companies = simple_load_companies("Members.csv")
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
                    row = line.decode('utf-8').rstrip()
                    if company.date_from <= datetime.strptime(row[0:10], '%Y-%m-%d').date() <= company.date_to:
                        csvfile.write(line.decode('utf-8').rstrip()+'\n')


if __name__ == "__main__":
    macro_trends_retriever()

