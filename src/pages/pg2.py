# App2
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import dash_mantine_components as dmc
import requests
import json

dash.register_page(__name__, name='County Map: % Indicators')

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
                html.P('Select Indicator:', style={'font-size': '15px', 'color': '#34495E', 'margin-top': '8px'}),
                dcc.Dropdown(
                    id='indicator-selector2',
                    options=[
                        {'label': 'Percentage of PWS population receiving fluoridated water',
                         'value': 'Percentage of PWS population receiving fluoridated water'},
                        {
                            'label': 'Percentage of PWS population receiving fluoridated water from PWS adjusting fluoride',
                            'value': 'Percentage of PWS population receiving fluoridated water from PWS adjusting fluoride'},
                        {
                            'label': 'Percentage of PWS population receiving fluoridated water from PWS with natural fluoride at or above the recommended level',
                            'value':
                                'Percentage of PWS population receiving fluoridated water from PWS with natural fluoride at or above the recommended level'},
                        {
                            'label': 'Percentage of PWS population receiving fluoridated water from PWS consecutive to systems with optimal fluoride levels',
                            'value':
                                'Percentage of PWS population receiving fluoridated water from PWS consecutive to systems with optimal fluoride levels'},
                        {
                            'label': 'Percentage of PWS population receiving water from PWS with less than the recommended level',
                            'value':
                                'Percentage of PWS population receiving water from PWS with less than the recommended level'}
                    ],
                    value='Percentage of PWS population receiving fluoridated water',
                    className='mb-2',
                    style={'color': '#2A52BE', 'font-size': '14px'},
                ),
            ]),
            width={"size": 11, "offset": 0},
        ),
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Button("Update Graph", id='update-button2', color='primary', n_clicks=0,
                       style={'width': '120px', 'height': '30px', 'font-size': '12px', 'padding': '2px'})
        ),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='choropleth-map2', style={'margin-top': '6px', 'width': '80%', 'height': '62vh'},
                          ),
                ),
    ]),

    dbc.Col(
        dmc.Center(
            children=[
                dmc.Image(
                    src='https://myhealth.alberta.ca/Alberta/Alberta%20Images/10-fluoride-facts/fluoride-facts-graphic-03.jpg',
                    alt="Water Fluoridation Reporting System",
                    width=100,
                    height=50,
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
    dash.dependencies.Output('choropleth-map2', 'figure'),
    [dash.dependencies.Input('indicator-selector2', 'value'),
     dash.dependencies.Input('update-button2', 'n_clicks')],
    prevent_initial_call=True,
)
def update_map(selected_indicator2, n_clicks):
    if n_clicks == None:
        raise PreventUpdate

    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=df.fips,
        z=df[selected_indicator2],
        colorscale='Viridis',
        zmin=0,
        zmax=max(df[selected_indicator2]),
        marker_opacity=0.5,
        marker_line_width=0,
        hoverinfo="location+z",
        customdata=df['name'],
        hovertemplate="name:%{customdata}<br>" + selected_indicator2 + ": %{z}<extra></extra>",
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3,
        mapbox_center={"lat": 37.0902, "lon": -97.7129},
    )

    return fig
