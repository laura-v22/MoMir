import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.SANDSTONE, dbc.icons.FONT_AWESOME]
)

app.layout = dbc.Row([
    dbc.Col([
        html.Div([
        html.Br(),
        dbc.Stack([
            html.Div(
                dcc.Link(html.Img(src='assets/miracoli.jpg', height=200), href='/')
            ),
            html.Div([
                html.H1('MoMir'),
                html.H3('Monitoring data from Piazza dei Miracoli'),
                html.Div([
                    html.Div(dcc.Link('Home - /', href='/')),
                    html.Div(dcc.Link('Baptistery - /baptistery', href='/baptistery')),
                    html.Div(dcc.Link('Square - /square', href='/square')),
                    html.Div(dcc.Link('Tower - /tower', href='/tower'))
                ])
            ]),
        ],
            direction='horizontal', gap=3
        ),
        html.Br(),
        dash.page_container
        ])
    ], lg=dict(width=10, offset=1)
    ),
    dbc.Col(width=1)
])

if __name__ == '__main__':
    app.run(debug=True, port=8051)
