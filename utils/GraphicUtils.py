import enum
from datetime import date
from typing import NamedTuple, List

import plotly.graph_objects as go
import pandas as pd

TRADER_X_AXIS_TEXT = "End of green line - buy date. End of red line - sell date."


class Colors(enum.Enum):
    green = 1
    red = 2
    blue = 3


class Line(NamedTuple):
    x0: date
    y0: float
    x1: date
    y1: float
    color: str


def draw_candlestick_chart(path: str, company: str, lines: List[Line], x_title: str):
    df = pd.read_csv(path + company)
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'],
                                         increasing_line_color='white',
                                         decreasing_line_color='black')])
    fig.update_layout(
        title=company[0:len(company) - 4],
        yaxis_title=company[0:len(company) - 4] + ' stocks price',
        xaxis_title=x_title)

    for line in lines:
        fig.add_shape(
            # Line Diagonal
            go.layout.Shape(
                type="line",
                x0=line.x0,
                y0=line.y0,
                x1=line.x1,
                y1=line.y1,
                line=dict(
                    color=line.color,
                    width=1,
                )
            ))
    fig.show()
