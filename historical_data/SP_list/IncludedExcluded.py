from typing import NamedTuple
from datetime import date, datetime


class IncludedExcludedEvent(NamedTuple):
    date: date
    included: str
    excluded: str


def load_included_excluded(file_name):
    import numpy as np
    date, included, excluded = np.loadtxt(
        file_name,
        delimiter=',',
        usecols=(0, 1, 2),
        unpack=True,
        skiprows=1,
        dtype='datetime64[D], str, str')

    out = []

    for date_val, included_val, excluded_val in \
            zip(date, included, excluded):
        out.append(IncludedExcludedEvent(
            date=date_val,
            included=included_val,
            excluded=excluded_val)
        )

    return out

def main():
    included_excluded_list = load_included_excluded("IncludedExcluded.csv")
    included_dict = {}
    for event in included_excluded_list:
        included_dict[str(event.included)]=str(event.date)
    for event in included_excluded_list:
        if included_dict.__contains__(event.excluded):
            #company,date_from,date_to
            print(event.excluded+','+
                  dict.get(event.excluded, '2000-01-01')+','+
                  str(event.date))

if __name__ == "__main__":
    main()
