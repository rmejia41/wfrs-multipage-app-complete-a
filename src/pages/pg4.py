# App 4
import dash
from dash import html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
import dash_mantine_components as dmc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import plotly

dash.register_page(__name__, path='/', name='Home: State Fluoridation Trend') # '/' is home page

df = pd.read_csv('https://github.com/rmejia41/open_datasets/raw/main/wfrs_app_yearly_scatter.csv')

# select the Bootstrap stylesheet and figure template for the theme here:
# template_theme = "SANDSTONE"
# url_theme = dbc.themes.SANDSTONE
# # -----------------------------
#
# app = dash.Dash(__name__, external_stylesheets=[url_theme])
# load_figure_template(template_theme)

# Define the app layout using dbc.Container - #4169E1
layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1('WFRS Multipage Dashboard', style={'font-size': '40px', 'color': '#2A52BE'},
                        className='text-center text-primary mb-1'),  # mb-4 is the spacing between titles
                width=12)
    ),

    dbc.Row(
        dbc.Col(html.H4('Centers for Disease Control and Prevention, Division of Oral Health',
                        style={'font-size': '20px', 'color': '#2A52BE'},
                        className='text-center text-primary mb-2'),
                width=12)
    ),

    html.Br(),

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(id='dpdn2', value=['Alabama', 'Arkansas'], multi=True,
                         options=[{'label': x, 'value': x} for x in df.state.unique()
                                  ]),
            html.Br(),

            dbc.Row([
                dcc.Graph(id='pie-graph', figure={}, className='six columns', style=
                {'width': '40%', 'height': '500px'}),
                dcc.Graph(id='my-graph', figure={}, clickData=None, hoverData=None,
                          config={
                              'staticPlot': False,  # True, False
                              'scrollZoom': True,  # True, False
                              'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                              'showTips': True,  # True, False
                              'displayModeBar': True,  # True, False, 'hover'
                              'watermark': True,
                              # 'modeBarButtonsToRemove': ['pan2d','select2d'],
                          },
                          className='six columns',
                          style={'width': '60%', 'height': '500px'}),
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
                        "marginTop": 10,
                        "marginBottom": 20,
                    },
                ),
            ],
        ),
    ),

            dbc.Row([
                html.A("Explore Fluoridation Statistics, CDC/DOH",
                       href="https://www.cdc.gov/fluoridation/statistics/reference_stats.htm",
                       target="_blank", style={'font-size': '13px', 'color': '#34495E', 'text-align': 'center'}),
            ]),
        ])
    ]),
])


@callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(state_chosen):
    dff = df[df.state.isin(state_chosen)]
    fig = px.scatter(data_frame=dff, x='year', y='pop_cws_fl', color='state',
                     labels={
                         "pop_cws": "CWS Population",
                         "pop_fl_water": "Fluoridated Water Population",
                         "region": "Region",
                         "state": "State",
                         "pop_cws_fl": "% Population Fluoridated Water"
                     },
                     custom_data=['state', 'region'])
    fig.update_traces(mode='lines+markers')
    return fig


# Dash version 1.16.0 or higher
@callback(
    Output(component_id='pie-graph', component_property='figure'),
    Input(component_id='my-graph', component_property='hoverData'),
    Input(component_id='my-graph', component_property='clickData'),
    Input(component_id='my-graph', component_property='selectedData'),
    Input(component_id='dpdn2', component_property='value')
)
def update_side_graph(hov_data, clk_data, slct_data, state_chosen):
    if hov_data is None:
        dff2 = df[df.state.isin(state_chosen)]
        dff2 = dff2[dff2.year == 2020]
        print(dff2)
        fig2 = px.pie(data_frame=dff2, values='pop_cws_fl', names='state',
                      labels={  # replaces default labels by column name
                          "state": "State", "region": "Region", "pop_fl_water": "Fluoridated Water Population",
                          "pop_cws_fl": "% Population Fluoridated Water"},
                      title='% CWS Population Served with Fluoridated Water')
        return fig2
    else:
        print(f'hover data: {hov_data}')
        # print(hov_data['points'][0]['customdata'][0])
        # print(f'click data: {clk_data}')
        # print(f'selected data: {slct_data}')
        dff2 = df[df.state.isin(state_chosen)]
        hov_year = hov_data['points'][0]['x']
        dff2 = dff2[dff2.year == hov_year]
        fig2 = px.pie(data_frame=dff2, values='pop_fl_water', names='state',
                      labels={  # replaces default labels by column name
                          "state": "State", "region": "Region", "pop_fl_water": "Fluoridated Water Population",
                          "pop_cws_fl": "% Population Fluoridated Water"
                      })
        return fig2