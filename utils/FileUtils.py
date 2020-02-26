from datetime import datetime

from historical_data.Quote import Quote


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