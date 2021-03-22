import dash
import dash_bootstrap_components as dbc
import pandas as pd

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

primaryDf = pd.read_json("Data/mergefile.txt.zip", lines=True, orient='Table')
primaryDf = primaryDf.loc[primaryDf['JSON_SAMPLE_TYPE'] == 'COMPLETE']
primaryDf['TIMESTAMP'] = primaryDf['TIMESTAMP'].astype(str).str[:-5]
primaryDf["TIMESTAMP"] = pd.to_datetime(primaryDf["TIMESTAMP"], format="%Y-%m-%d %H.%M.%S", exact=True)
primaryDf.reset_index(drop=True, inplace=True)
boolIdx = primaryDf['SUMMARY'].apply(lambda summObj: summObj['totalMem[KB]'] == 0)
indexNames = primaryDf[boolIdx].index
primaryDf.drop(indexNames, inplace=True)
timeDf = primaryDf[["TIMESTAMP", 'HOSTNAME']]
summarydf = pd.DataFrame(primaryDf['SUMMARY'].values.tolist())
summarydf[['TIMESTAMP', 'HOSTNAME']] = timeDf
