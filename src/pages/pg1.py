# App1
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import dash_mantine_components as dmc

dash.register_page(__name__, name='State Fluoridation Map')

df = pd.read_csv('https://github.com/rmejia41/open_datasets/raw/main/wfrs_states.csv')

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1('WFRS State-Level Dashboard',
                        style={'font-size': '40px', 'color': '#2A52BE'},
                        className='text-center text-primary mb-1'),  # mb-4 is the spacing between titles
                width=12)
    ),

    dbc.Row(
        dbc.Col(html.H4('Centers for Disease Control and Prevention, Division of Oral Health',
                        style={'font-size': '20px', 'color': '#2A52BE', 'font-family': 'Raleway'},
                        className='text-center text-primary mb-4'),
                width=12)
    ),

    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value': year} for year in [2016, 2018, 2020]],
                value=None,
                placeholder='Select Year',
                className='mb-2',
                style={'color': '#2A52BE', 'font-size': '14px'},
            ),
            width={'size': 6}
        ),

        dbc.Col(
            dcc.Dropdown(
                id='percentage-dropdown',
                options=[
                    {"label": "Percentage of PWS population receiving fluoridated water",
                     "value": "percent_pws_pop_fl_water"},
                    {"label": "Percentage of PWS population receiving fluoridated water from PWS adjusting fluoride",
                     "value": "percent_pws_pop_ fl_water_pws_adjust_fl"},
                    {
                        'label': 'Percentage of PWS population receiving fluoridated water from PWS with natural fluoride at or above the recommended level',
                        'value':
                            'percent_pws_pop_fl_water_pws_natural_fl _at_above_recom_level'},
                    {
                        'label': 'Percentage of PWS population receiving fluoridated water from PWS consecutive to systems with optimal fluoride levels',
                        'value':
                            'percent_pop_fl_water_pws_consecutive_optimal_fl'},
                    {
                        'label': 'Percentage of PWS population receiving water from PWS with less than the recommended level',
                        'value':
                            'percent_pws_pop_water_pws_less_recom_level'}
                ],
                value=None,
                placeholder='Select Indicator',
                className='mb-1',
                style={'color': '#2A52BE', 'font-size': '14px'},
            ),
            width={"size": 11, "offset": 0},
        ),
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Button("Update Graph", id='update-button', color='primary', n_clicks=0,
                       style={'width': '120px', 'height': '30px', 'font-size': '12px', 'padding': '2px'})
        )
    ]),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id='choropleth-graph'),
            width={'size': 12}
        ),
    ]),

    dbc.Col(
        dmc.Center(
            children=[
                dmc.Image(
                    src='https://www.cdc.gov/fluoridation/images/wfrs-logo-210px.jpg?_=03553',
                    alt="Water Fluoridation Reporting System",
                    width=160,
                    height=90,
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
    Output('choropleth-graph', 'figure'),
    [Input('update-button', 'n_clicks'),
     Input('year-dropdown', 'value'),
     Input('percentage-dropdown', 'value')],
    prevent_initial_call=True,
)
def update_choropleth_graph(n_clicks, selected_year, selected_percentage):
    if n_clicks == None:
        raise PreventUpdate
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] == 'update-button.n_clicks':
        filtered_df = df[(df['year'] == selected_year)][['jurisdiction', selected_percentage]]

        fig = px.choropleth(
            filtered_df,
            locations='jurisdiction',
            locationmode='USA-states',
            scope="usa",
            color=selected_percentage,
            color_continuous_scale='Plasma',
            labels={'percent_pws_pop_fl_water': '% of PWS population: Fluoridated Water',
                    'percent_pws_pop_ fl_water_pws_adjust_fl': '% of PWS population: Adjusting fluoride',
                    'percent_pws_pop_fl_water_pws_natural_fl _at_above_recom_level': '% PWS population: Natural fluoride',
                    'percent_pop_fl_water_pws_consecutive_optimal_fl': '% PWS population: Consecutive optimal fluoride',
                    'percent_pws_pop_water_pws_less_recom_level': '% PWS population: Less than recommended level'
                    },
            #title=f"{selected_percentage} in {selected_year}"
            # template='plotly_dark'
        )

    return fig
