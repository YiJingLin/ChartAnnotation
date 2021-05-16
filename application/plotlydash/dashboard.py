"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go


# from .data import create_dataframe
from .layout import html_layout


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
            'https://fonts.googleapis.com/css?family=Lato'
        ]
    )
    
    # example data
    import random
    x = np.arange(30)
    y = [ e * 5 * random.randint(3, 10) for e in x]
    
    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            dcc.Graph(
                id='line-chart',
                figure = go.Figure(data=[go.Scatter(x=x, y=y)])
            ),
            dcc.RangeSlider(
                id = 'range-slider',
                marks={i: 't{}'.format(i) for i in range(len(x))},
                min=x[0],
                max=x[-1],
                value=[x[0], x[-1]]
            ),
            html.Button('Submit', id='button'),
            html.Div(id='output-container-button',
             children='Enter a value and press submit')
#             dcc.Graph(
#                 id='line2',
#                 figure = go.Figure(data=[go.Scatter(x=x, y=x**2)])
#             ),
#             dcc.RangeSlider(
#                 id = 'rs2',
#                 marks={i: 'Label {}'.format(i) for i in range(-5, 7)},
#                 min=-5,
#                 max=6,
#                 value=[-3, 4]
#             ),
        ],
        id='dash-container'
    )

    init_callbacks(dash_app, x, y)

    return dash_app.server


def init_callbacks(dash_app, x, y):
    @dash_app.callback(
        Output("line-chart", "figure"), 
        [Input("range-slider", "value")])
    def update_line_chart(range_value):
        start, end = range_value
        print(start, end)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y))
        fig.add_trace(go.Scatter(x=[start, end], y=[y[start], y[end]]))
        return fig
    
    @dash_app.callback(
        Output('output-container-button', 'children'),
        [Input('button', 'n_clicks')],
        [State('range-slider', 'value')])
    def save_line(n_clicks, value):
        x_start, x_end = value
        y_start, y_end = y[x_start], y[x_end]
#         print('start: ({}, {}), end: ({}, {})'.format(x_start, y_start, x_end, y_end))
        return 'start point: ({}, {}), end point: ({}, {}) saved'.format(x_start, y_start, x_end, y_end)