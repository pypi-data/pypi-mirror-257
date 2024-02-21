import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, html, dcc
from datetime import datetime, timedelta


def start_webserver():
    """
    Starts a local instance of a Dash application on default host
    https://127.0.0.1:8050
    :return: Nothing
    """

    app.run_server(port=8050, debug=True)


time_zone_offsets = {
    'Eastern Standard Time (EST)': 0,
    'Coordinated Universal Time (UTC)': -5,
    'Central European Time (CET)': -6,
    'Pacific Standard Time (PST)': +3,
    'Australian Eastern Standard Time (AEST)': +15,
    'Japan Standard Time (JST)': +14,
    'Greenwich Mean Time (GMT)': -5,
    'India Standard Time (IST)': +10.5,
    'China Standard Time (CST)': +13,
    'Eastern European Time (EET)': -7,
}

search_bar = dbc.Row(
    [
        dcc.Dropdown(id='timezone-selector',
                     value='Eastern Standard Time (EST)',
                     options=[key for key in time_zone_offsets.keys()],
                     placeholder='Select a Timezone',
                     style={'width': '20em'})
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Current Time", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),
            search_bar
        ]
    ),
    color="dark",
    dark=True,
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    navbar,
    html.Br(),
    dbc.Row(
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H3(id='timezone-header')),
                    html.Br(),
                    dbc.Row(html.H5(id='time-in-timezone')),
                    html.Br()
                ]
            )
        )
    )
])


@app.callback(
    [Output('timezone-header', 'children'),
     Output('time-in-timezone', 'children')],
    Input('timezone-selector', 'value')
)
def return_timezone(val):

    if val:
        current_time = (datetime.now() - timedelta(hours=time_zone_offsets[val])).strftime("%m/%d/%Y %H:%M:%S")
        return val, current_time
    else:
        return 'Eastern Standard Time (EST)', datetime.now().strftime("%m/%d/%Y %H:%M:%S")

if __name__ == '__main__':
    start_webserver()

