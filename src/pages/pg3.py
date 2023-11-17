# App3
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from urllib.request import urlopen
from PIL import Image
import dash_mantine_components as dmc
import json
import requests
import os

dash.register_page(__name__, name='County Map: PWS Counts')

url = "https://github.com/rmejia41/open_datasets/raw/main/counties.json"
response = requests.get(url)
geojson_data = response.json()

df = pd.read_csv('https://github.com/rmejia41/open_datasets/raw/main/county_pivot.csv')

# Create the Dash app with Bootstrap - SANDSTONE
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

# Define the app layout using dbc.Container - #4169E1
layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1('WFRS County Dashboard', style={'font-size': '40px', 'color': '#2A52BE'},
                        className='text-center text-primary mb-1'),  # mb-4 is the spacing between titles
                width=12)
    ),

    dbc.Row(
        dbc.Col(html.H4('Centers for Disease Control and Prevention, Division of Oral Health',
                        style={'font-size': '20px', 'color': '#2A52BE'},
                        className='text-center text-primary mb-2'),
                width=12)
    ),

    dbc.Row([
        dbc.Col(
            html.Div([
                html.P('Select PWS Type and Metric:',
                       style={'font-size': '15px', 'color': '#34495E', 'margin-top': '8px'}),
                dcc.Dropdown(
                    id='count-selector3',
                    options=[
                        {'label': 'Fluoridated: Number of PWS providing fluoridated water',
                         'value': 'Number of PWS providing fluoridated water'},
                        {'label': 'Adjusted: Number of PWS adjusting fluoride',
                         'value': 'Number of PWS adjusting fluoride'},
                        {'label': 'Consecutive: Number of PWS consecutive to systems with optimal fluoride levels',
                         'value': 'Number of PWS consecutive to systems with optimal fluoride levels'},
                        {'label': 'None-Fluoridated: Number of PWS with fluoride below the recommended level',
                         'value': 'Number of PWS with fluoride below the recommended level'},
                        {'label': 'Natural: Number of PWS with naturally occurring fluoride at or above optimal levels',
                         'value':
                             'Number of PWS with naturally occurring fluoride at or above optimal levels'},
                        {'label': 'Total number of PWS', 'value': 'Total number of PWS'}
                    ],
                    value='Number of PWS providing fluoridated water',
                    className='mb-2',
                    style={'color': '#2A52BE', 'font-size': '14px'},
                    # style={'background-color':'#30E3DF'}
                ),
            ]),
            width={"size": 10, "offset": 0},
        ),
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Button("Update Graph", id='update-button3', color='primary', n_clicks=0,
                       style={'width': '120px', 'height': '30px', 'font-size': '12px', 'padding': '2px'})
        )
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='choropleth-map3', style={'margin-top': '6px', 'width': '100%', 'height': '62vh'},
                          ),
                ),
    ]),

    dbc.Col(
        dmc.Center(
            children=[
                dmc.Image(
                    src='https://now.tufts.edu/sites/default/files/styles/large_1366w_912h/public/uploaded-assets/images/2022-08/110226_ask_fluoride_hero.jpg?h=e5aec6c8&itok=jaIb6hJP',
                    alt="Water Fluoridation Reporting System",
                    width=130,
                    height=80,
                    style={
                        # "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
                        "marginTop": -15,
                        "marginBottom": 20,
                    },
                ),
            ],
        ),
    ),

    dbc.Row([
        html.A("Download Oral Health Data, CDC/DOH", href="https://nccdqa.cdc.gov/oralhealthdata/rdPage.aspx",
               target="_blank", style={'font-size': '13px', 'color': '#34495E', 'text-align': 'center'}),

    ]),
])


@callback(
    dash.dependencies.Output('choropleth-map3', 'figure'),
    [dash.dependencies.Input('count-selector3', 'value'),
     dash.dependencies.Input('update-button3', 'n_clicks')],
    prevent_initial_call=True,
)
def update_map(selected_count3, n_clicks):
    if n_clicks == None:
        raise PreventUpdate

    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=df.fips,
        z=df[selected_count3],
        colorscale='Viridis',
        zmin=0,
        zmax=200,
        marker_opacity=0.5,
        marker_line_width=0,
        hoverinfo="location+z",
        customdata=df['name'],
        hovertemplate="name:%{customdata}<br>" + selected_count3 + ": %{z}<extra></extra>",
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3,
        mapbox_center={"lat": 37.0902, "lon": -97.7129},
    )

    return fig
