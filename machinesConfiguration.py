from plotly import graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
from app import app
from app import summarydf


summarydf = summarydf.groupby('HOSTNAME').head(1)
summarydf.reset_index(drop=True, inplace=True)
summarydf = summarydf[['HOSTNAME', 'cores[#]', 'totalMem[KB]', 'swapTotal[KB]', 'disks[#]', 'nics[#]']]


def machinesConfig():
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(summarydf.columns),
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[summarydf['HOSTNAME'], summarydf['cores[#]'], summarydf['totalMem[KB]'], summarydf['swapTotal[KB]'],
                           summarydf['disks[#]'], summarydf['nics[#]']],
                   fill_color='lavender',
                   align='center'))
    ])

    layout = dbc.Container([

        dbc.Row(
            dbc.Col(html.H2("Machines Configuration",
                            className='text-center text-primary mb-4'),
                    width=12)
        ),
        dbc.Row([dbc.Col([
            dcc.Graph(id='line-fig2', figure=fig)
        ], xs=12, sm=12, md=12, lg=12, xl=12), ], no_gutters=True, justify='start', align='center'),

    ], fluid=True)

    return layout

