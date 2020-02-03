import pandas as pd
import wikipedia as wp

from dateutil.parser import parse
import math

html = wp.page("List of S&P 500 companies").html().encode("UTF-8")
df = pd.read_html(html)[1]
rows, columns = df.shape

i = 2

dates = {}
current_date = None
while i < rows:
    try:
        current_date = parse(str(df.at[i, 0]))
        action = {}
        action["Add"] = []
        action["Remove"] = []
        if not isinstance(df.at[i, 1], float):
            action["Add"].append(df.at[i, 1])
        if not isinstance(df.at[i, 3], float):
            action["Remove"].append(df.at[i, 3])
        dates[current_date] = action
    except ValueError:
        dates[current_date]["Add"].append(df.at[i, 0])
        if not isinstance(df.at[i, 2], float):
            dates[current_date]["Remove"].append(df.at[i, 2])
    i += 1

print(dates)