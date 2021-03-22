from plotly import graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
from app import app

from app import summarydf

# print(summarydf.head(5))

metricList1 = ['usage[%]', 'user[%]', 'system[%]']
metricList2 = ['cpuQ[#]', 'procs[#]']

hostlist = summarydf['HOSTNAME'].unique()


def cpuAnalyser():
    layout = dbc.Container([

        dbc.Row(
            dbc.Col(html.H2("CPU Dashboard",
                            className='text-center text-primary mb-4'),
                    width=12)
        ),

        dbc.Row([
            dbc.Col([
                html.P("Select metric from below drop down:",
                       style={"textDecoration": "bold"}),
                dcc.Dropdown(id='metric-dropdown1', multi=False, value=metricList1[0],
                             options=[{'label': x, 'value': x}
                                      for x in metricList1], style={"width": "50%", 'margin': 'left', 'verticalAlign':'left'}
                             ),
            ],  # width={'size':5, 'offset':1, 'order':1},
                xs=12, sm=3, md=12, lg=5, xl=5
            ),

            dbc.Col([
                html.P("Select host from below drop down:",
                       style={"textDecoration": "bold"}),

                dcc.Dropdown(id='host-dropdown1', multi=False, value=hostlist[0],
                             options=[{'label': x, 'value': x}
                                      for x in hostlist], style={"width": "50%", 'margin': 'left'},
                             ),

            ],  # width={'size':5, 'offset':1, 'order':1},
                xs=12, sm=3, md=12, lg=5, xl=5
            ),
        ], no_gutters=True, justify='start'),  # Horizontal:start,center,end,between,around

        dbc.Row([dbc.Col([
            dcc.Graph(id='line-fig1', figure={})
        ], xs=12, sm=3, md=12, lg=12, xl=12),], no_gutters=True, justify='start', align='center'),

        dbc.Row([
            dbc.Col([
                html.P("Select metric from below drop down:",
                       style={"textDecoration": "bold"}),
                dcc.Dropdown(id='metric-dropdown2', multi=False, value=metricList2[0],
                             options=[{'label': x, 'value': x}
                                      for x in metricList2],
                             style={"width": "50%", 'margin': 'left', 'verticalAlign': 'left'}
                             ),
            ],  # width={'size':5, 'offset':1, 'order':1},
                xs=12, sm=3, md=12, lg=5, xl=5
            ),

            dbc.Col([
                html.P("Select host from below drop down:",
                       style={"textDecoration": "bold"}),

                dcc.Dropdown(id='host-dropdown2', multi=True, value=[hostlist[0]],
                             options=[{'label': x, 'value': x}
                                      for x in hostlist], style={"width": "50%", 'margin': 'left'},
                             ),
            ],  # width={'size':5, 'offset':1, 'order':1},
                xs=12, sm=3, md=12, lg=5, xl=5
            ),
        ], no_gutters=True, justify='start'),  # Horizontal:start,center,end,between,around

        dbc.Row([dbc.Col([
            dcc.Graph(id='line-fig2', figure={})
        ], xs=12, sm=3, md=12, lg=12, xl=12), ], no_gutters=True, justify='start', align='center'),

    ], fluid=True)

    return layout


@app.callback(
    Output(component_id='line-fig1', component_property='figure'),
    [Input(component_id='metric-dropdown1', component_property='value'),
     Input(component_id='host-dropdown1', component_property='value')]
)
def display_value(metric, host):

    displaydf = summarydf.loc[summarydf['HOSTNAME'] == host]
    displaydf = displaydf[['TIMESTAMP', metric]]
    displaydf.reset_index(drop=True, inplace=True)

    trace0 = go.Scatter(x=displaydf['TIMESTAMP'], y=displaydf[metric], name=metric)
    data = [trace0]
    title = '{host} {metric} chart'.format(host=host, metric=metric)
    layout = dict(title=title,
                  # plot_bgcolor='pink',
                  # paper_bgcolor='black',
                  font={'color':'maroon'},
                  xaxis=dict(title='Time'),
                  yaxis=dict(title='%'),
                  autosize=True,
                  # width=500,
                  # height=500,
                  )
    fig = dict(data=data, layout=layout)
    fig['data'][0]['showlegend'] = True
    return fig


# Line chart - multiple
@app.callback(
    Output(component_id='line-fig2', component_property='figure'),
    [Input(component_id='metric-dropdown2', component_property='value'),
     Input(component_id='host-dropdown2', component_property='value')]
)
def display_value(metric, hosts):
    # print('Hosts are: '+ hosts)
    # print('Host type is : '+str(type(hosts)))
    traceList = []
    for host in hosts:
        # print(summarydf.head(10))
        displaydf = summarydf.loc[summarydf['HOSTNAME'] == host]
        displaydf = displaydf[['TIMESTAMP', metric]]
        displaydf.reset_index(drop=True, inplace=True)

        traceList.append(go.Scatter(x=displaydf['TIMESTAMP'], y=displaydf[metric], name=host))

    data = traceList
    title = '{metric} chart'.format(metric=metric)
    layout = dict(title=title,
                  # plot_bgcolor='pink',
                  # paper_bgcolor='black',
                  font={'color':'maroon'},
                  xaxis=dict(title='Time'),
                  yaxis=dict(title='%'),
                  autosize=True,
                  # width=500,
                  # height=500,
                  )
    fig = dict(data=data, layout=layout)
    fig['data'][0]['showlegend'] = True

    # dff = summarydf[summarydf['HOSTNAME'].isin(hosts)]
    # fig = px.line(dff, x='TIMESTAMP', y=metric)
    return fig
