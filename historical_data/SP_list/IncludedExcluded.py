from typing import NamedTuple
from datetime import date, datetime


class IncludedExcludedEvent(NamedTuple):
    date: date
    included_company: str
    excluded_company: str


def simple_load_companies(file_name):
    import csv
    out = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        out = []
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f"reading line {line_count}")
                out.append(IncludedExcludedEvent(
                    date=datetime.strptime(row[0], '%Y-%m-%d').date(),
                    included_company=str(row[1]),
                    excluded_company=str(row[2]))
                )
                line_count += 1
    return out

def main():
    included_excluded_list = simple_load_companies("IncludedExcluded.csv")
    included_dict = {}
    for event in included_excluded_list:
        included_dict[str(event.included_company)]=str(event.date)
    for event in included_excluded_list:
        #company,date_from,date_to
        print(event.excluded_company+','+
              included_dict.get(event.excluded_company, '2000-01-01')
              +','+str(event.date))

if __name__ == "__main__":
    main()
