import os, shutil, enum
from datetime import date, timedelta
from typing import List

from historical_data.Quote import Quote, CSV_HEADER_ROW_WITH_GICS
from snippets.SnippetConfiguration import PERIOD_OF_GROWTH_OR_FALL_AFTER_SNIPPET_IN_DAYS, NUMBER_OF_ROWS_IN_SNIPPET_FILE

PATH_TO_SNIPPETS = '../snippets/snippets_data/'
SNIPPET_X_AXIS_TEXT = "After green = buy, after red = sell, after blue = hold"


# Using enum class create enumerations
class SnippetTypes(enum.Enum):
    buy = 1
    sell = 2
    hold = 3


def less_than_interval(date_from: date, date_to: date) -> bool:
    return date_to - date_from < timedelta(days=PERIOD_OF_GROWTH_OR_FALL_AFTER_SNIPPET_IN_DAYS)


def create_snippet(quotes: List[Quote], right_border: int, snippet_type: SnippetTypes, gics: int, company: str):
    left_border = right_border - NUMBER_OF_ROWS_IN_SNIPPET_FILE
    write_snippet_to_csv_file(quotes[left_border:right_border], snippet_type, gics, company)
    return [left_border, right_border, snippet_type]


def write_snippet_to_csv_file(quotes: List[Quote], snippet_type: SnippetTypes, gics: int, company: str):
    with open(get_next_file_path(PATH_TO_SNIPPETS + company + '/' + snippet_type.name) + '.csv', 'w') as csv_file:
        csv_file.write(str(CSV_HEADER_ROW_WITH_GICS))
        for quote in quotes:
            csv_file.write(str(quote.date) + ',' + str(quote.open_price) + ',' + str(quote.high_price) + ','
                           + str(quote.low_price) + ',' + str(quote.close_price) + ','
                           + str(quote.adj_close_price) + ',' + str(quote.volume) + ',' + str(gics) + '\n')


def get_next_file_path(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
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


def analyze_to(quotes: List[Quote]) -> int:
    last = len(quotes) - 1
    pointer = last
    while less_than_interval(quotes[pointer].date, quotes[last].date):
        pointer -= 1
        if pointer == -1:
            return 0
    return pointer + 1


def clear_snippets_directory():
    folder = PATH_TO_SNIPPETS
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
