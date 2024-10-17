import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Home'),
    html.Div(
        [
            dcc.Markdown(
                """
                *work in progress*

                The dashboard is licensed under the [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).

                The source code can be found [here](https://github.com/carloresta/momir).
                """
            )
        ]
    ),
    #html.Iframe(
        #src="http://www.maxmartino.it/torre/index.htm",  # Link al sito da includere
        #src='https://it.wikipedia.org/wiki/Piazza_dei_Miracoli',
        #style={"width": "100%", "height": "600px", "border": "none"}  # Dimensioni e stile dell'iframe
        #style={"width": "100%", "height": "600px", "border": "none"}  # Dimensioni e stile dell'iframe
    #),
  
    
 
])
