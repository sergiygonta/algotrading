import pandas as pd
import wikipedia as wp

sp_500_current = []

# Get the html source
html = wp.page("List of S&P 500 companies").html().encode("UTF-8")
df = pd.read_html(html)[0]
for key, row in df.iterrows():
    sp_500_current.append(row["Symbol"])

print(len(sp_500_current), sp_500_current)