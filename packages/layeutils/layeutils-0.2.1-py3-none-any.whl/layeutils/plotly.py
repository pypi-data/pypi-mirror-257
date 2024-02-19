import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


def dual_axis_plotly_line(data_df: pd.DataFrame, l1_col: str, l2_col: str, title: str = None) -> Figure:
    trace1 = go.Scatter(
        x=data_df.index,
        y=data_df[l1_col],
        name=data_df[l1_col].name
    )
    trace2 = go.Scatter(
        x=data_df.index,
        y=data_df[l2_col],
        name=data_df[l2_col].name,
        xaxis='x',
        yaxis='y2'  # 标明设置一个不同于trace1的一个坐标轴
    )
    data = [trace1, trace2]
    layout = go.Layout(
        yaxis2=dict(anchor='x', overlaying='y', side='right'),
        template='plotly_dark',
        title=title if title else f'{data_df[l1_col].name} VS {data_df[l2_col].name}'
    )
    return go.Figure(data=data, layout=layout)


def plotly_simple_line(df: pd.DataFrame, x_series: list, y_series: list, title: str = '', template: str = 'plotly_dark') -> Figure:
    return px.line(
        data_frame=df,
        x=x_series,
        y=y_series,
        title=title,
        template='template')
