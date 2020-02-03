import pandas as pd
import wikipedia as wp

sp_500_current = []

# Get the html source
html = wp.page("List of S&P 500 companies").html().encode("UTF-8")
df = pd.read_html(html)[0]
for t in df[0][1:]:
    sp_500_current.append(t)

print(len(sp_500_current), sp_500_current)