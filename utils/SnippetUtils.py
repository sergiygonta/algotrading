import os, shutil, enum
from datetime import date, timedelta
from typing import List, Dict

from historical_data.Quote import Quote, CSV_HEADER_ROW_WITH_GICS
from snippets.SnippetConfiguration import NUMBER_OF_ROWS_IN_SNIPPET_FILE

PATH_TO_SNIPPETS = '../snippets/snippets_data/'
SNIPPET_X_AXIS_TEXT = "After green = buy, after red = sell, after blue = hold"

# MAP_KEYS
GICS = "gics"
SPLIT_POINT = "split_point"
QUOTES = "quotes"
COMPANY = "company"
SNIPPET_TYPE = "snippet_type"
CUSTOM_FILE_NAME = "custom_file_name"


# Using enum class create enumerations
class SnippetTypes(enum.Enum):
    buy = 1
    sell = 2
    hold = 3


def create_snippet(parameters: Dict):
    left_border = parameters[SPLIT_POINT] - NUMBER_OF_ROWS_IN_SNIPPET_FILE
    if CUSTOM_FILE_NAME in parameters.keys():
        file_name = get_directory_path(parameters[COMPANY]) + parameters[CUSTOM_FILE_NAME]+'.csv'
    else:
        file_name = get_next_file_path(
            get_directory_path(parameters[COMPANY]) + parameters[SNIPPET_TYPE].name) + '.csv'
    with open(file_name, 'w') as csv_file:
        csv_file.write(str(CSV_HEADER_ROW_WITH_GICS))
        for quote in parameters[QUOTES][left_border: parameters[SPLIT_POINT] + 1]:
            csv_file.write(str(quote.date) + ',' + str(quote.open_price) + ',' + str(quote.high_price) + ','
                           + str(quote.low_price) + ',' + str(quote.close_price) + ',' + str(quote.adj_close_price)
                           + ',' + str(quote.volume) + ',' + str(parameters[GICS]) + '\n')
    return {x: parameters[x] for x in parameters}


def get_directory_path(company_name):
    path = PATH_TO_SNIPPETS + company_name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


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
