import os, shutil, enum
from datetime import date, timedelta
from typing import List

from historical_data.Quote import Quote, CSV_HEADER_ROW

PATH_TO_SNIPPETS = '../snippets/snippets_data/'


# Using enum class create enumerations
class SnippetTypes(enum.Enum):
    buy = 1
    sell = 2
    hold = 3


def less_that_three_month_interval(date_from: date, date_to: date) -> bool:
    return date_to - date_from < timedelta(days=90)


def create_3month_snippet(quotes: List[Quote], right_border: int, snippet_type: SnippetTypes):
    left_border = right_border
    while less_that_three_month_interval(quotes[left_border].date, quotes[right_border].date):
        left_border -= 1
    write_snippet_to_csv_file(quotes[left_border:right_border + 1], snippet_type)
    return [left_border, right_border, snippet_type]


def write_snippet_to_csv_file(quotes: List[Quote], snippet_type: SnippetTypes):
    with open(get_next_file_path(PATH_TO_SNIPPETS + snippet_type.name) + '.csv', 'w') as csv_file:
        csv_file.write(CSV_HEADER_ROW)
        for quote in quotes:
            csv_file.write(str(quote.date) + ',' + str(quote.open_price) + ',' + str(quote.high_price) + ','
                           + str(quote.low_price) + ',' + str(quote.close_price) + ','
                           + str(quote.adj_close_price) + ',' + str(quote.volume) + '\n')


def get_next_file_path(output_folder):
    highest_num = 0
    for f in os.listdir(output_folder):
        if os.path.isfile(os.path.join(output_folder, f)):
            file_name = os.path.splitext(f)[0]
            try:
                file_num = int(file_name)
                if file_num > highest_num:
                    highest_num = file_num
            except ValueError:
                'The file name "%s" is not an integer. Skipping' % file_name

    return os.path.join(output_folder, str(highest_num + 1))


def analyze_from(quotes: List[Quote]) -> int:
    pointer = 0
    while less_that_three_month_interval(quotes[0].date, quotes[pointer].date):
        pointer += 1
        if pointer == len(quotes):
            return 999999999999
    return pointer


def analyze_to(quotes: List[Quote]) -> int:
    last = len(quotes) - 1
    pointer = last
    while less_that_three_month_interval(quotes[pointer].date, quotes[last].date):
        pointer -= 1
        if pointer == -1:
            return 0
    return pointer + 1


def clear_snippets_directories():
    for snippet_type in SnippetTypes:
        full_path = PATH_TO_SNIPPETS + snippet_type.name
        for filename in os.listdir(full_path):
            file_path = os.path.join(full_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
