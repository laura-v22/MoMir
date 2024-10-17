# package imports
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc


# local imports
from utils.utils import id_factory
from utils.utils import svg_config
id = id_factory('square')
from .functions import *
from data.square_data import *

# page registration
dash.register_page(
    __name__,
    path='/square',
    title='Monitoring data of Piazza dei Miracoli'
)


#==============
#    LAYOUT
#==============
# The layout is divided into Tabs. To make everything
# as clear as possible, the tabs are defined first,
# then recalled into the outer lebel.

#------------
#    TABS
#------------
# SQUARE HISTORY Tab
#---- Gantt and info regarding monitoring of the Piazza
s_tab_history = dbc.Tab([
    html.Div([html.Br(),
    html.P(
        "This tab contains info about terrestrial and satellite monitoring.",
        style=dict(color='grey', fontSize='small')
    )
    ]),
    dbc.Row([html.H3("Levelling and satellite GANTT"),
            dbc.Col([
                dcc.Graph(id=id('gantt')),
                html.Br(),
            ],
                width=10,
                align='center'
            ),
            dbc.Col([
                dcc.Markdown("**Measurements to show**"),
                dbc.Checklist(
                    id=id('checklist_gantt'),
                    options=[
                        'Square levelling',
                        #'Tower levelling',
                        'ERS','ENVISAT',
                        'Sentinel-1','COSMO-SkyMed'
                    ],
                    value=[
                        'Square levelling',
                        #'Tower levelling',
                        'ERS','ENVISAT',
                        'Sentinel-1','COSMO-SkyMed'
                    ],
                    inline=False
                    ),
                html.Br(),
            ],
                width=2,
                align='center'
            ),
    ], justify='center'
    ),
    html.H4('Sources and technical characteristics'),
    dbc.Table([
        html.Thead(
            html.Tr(
                [
                    html.Th("Dataset"),
                    html.Th("Source"),
                    html.Th("Nominal accuracy"),
                    html.Th("Documentation")
                ]
            )
        ),
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td("Cosmo-SkyMed"),
                        html.Td("NHAZCA¹"),
                        html.Td("± 1.00 mm/year"),
                        html.Td(html.A("link", href="https://earth.esa.int/eogateway/missions/cosmo-skymed", target="_blank"))
                    ]
                ),
                html.Tr(
                    [
                        html.Td("Sentinel-1"),
                        html.Td("NHAZCA¹"),
                        html.Td("± 1.50 mm/year"),
                        html.Td(html.A("link", href="https://sentinel.esa.int/web/sentinel/missions/sentinel-1", target="_blank"))
                    ]
                ),
                html.Tr(
                    [
                        html.Td("ENVISAT"),
                        html.Td("NHAZCA¹"),
                        html.Td("± 2.00 mm/year"),
                        html.Td(html.A("link", href="https://earth.esa.int/eogateway/missions/envisat", target="_blank"))
                    ]
                ),
                html.Tr(
                    [
                        html.Td("ERS"),
                        html.Td("NHAZCA¹"),
                        html.Td("± 2.00 mm/year"),
                        html.Td(html.A("link", href="https://earth.esa.int/eogateway/missions/ers", target="_blank"))
                    ]
                ),
                html.Tr(
                    [
                        html.Td("Levelling"),
                        html.Td("ASTRO Laboratory²"),
                        html.Td(""),
                        html.Td(html.A("link", href="https://arpi.unipi.it/handle/11568/1002453", target="_blank"))
                    ]
                ),
               
            ]
        )
    ]),
    dcc.Markdown(
        """
        ¹[Natural Hazards Control and Assessment](https://www.nhazca.it/en/), startup of the Rome Sapienza University.

        ²Astro Laboratory, Department of Civil and Industrial Engineering of the University of Pisa.
        
        3[EUROTEC PISA s.r.l.] (https://www.eurotecpisa.eu).
        """
    )

], label="MONITORING HISTORY"
)

#SQUARE PLAN Tab
s_tab_plan = dbc.Tab([
    html.Div([
        html.Br(),
        html.P(
            "This tab contains data regarding terrestrial levelling and satellite monitoring.",
            style=dict(color='grey', fontSize='small')
        ),
        html.H3("Plan view of levelling and SAR benchmarks"),
        dcc.Markdown(
            """
            Using the checklist on the side, it is possible to select which data sources to show: SAR scatterers (constellations ERS, ENVISAT, Sentinel-1 and COSMO-SkyMed) and levelling benchmarks.

            By selecting points it is possible to visualise displacement data, windowing it and changing sampling frequency. Points can be selected by clicking, or using the lasso tool in the top right multimedia bar.

            Satellite measurements are available in LOS (direct measurement) and vertical (elaborated) directions. Benchmarks considered *unreliable* are installed in walkways or otherwise unprotected locations.
            """
        ),
        html.Br(),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id=id('map_square'), config=svg_config),
            html.Br()
        ],
            width=10,
            align='center'
        ),
        dbc.Col([
            dcc.Markdown("**Displacements options**"),
            dbc.RadioItems(
                options=[
                    {"label": "LOS", "value": False},
                    {"label": "Vertical", "value": True},
                ],
                value=False,
                id=id("radioitems_map_square"),
            ),
            dcc.Markdown("**Benchmarks to show**"),
            dbc.Checklist(
                id=id('checklist_map_square'),
                options=[
                    'Lev. reliable',
                    'Lev. unreliable',
                    'ERS','ENVISAT',
                    'Sentinel-1','COSMO-SkyMed'
                ],
                value=['Lev. reliable'],
                inline=False
                ),
            html.Br(),
            dcc.Markdown("###### Coherence"),
            dcc.RangeSlider(
                id=id('rangeslider_map_square_coherence'),
                min=0.,
                max=1.,
                step=0.25,
                value=[0., 1.]
            ),
            dcc.Markdown("###### Height"),
            dcc.RangeSlider(
                id=id('rangeslider_map_square_height'),
                min=0,
                max=60,
                step=10,
                value=[0, 70]
            )
        ],
            width=2,
            align='center'
        )
    ],
        justify='center'),
        dcc.Markdown(id=id('number_points_map_square'), style={'white-space':'pre'}),
        html.Br(),
        html.Div(html.H2("Displacements of the points")),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dcc.Markdown('Superimpose the plots of all scatterers?'),
                dbc.Checklist(
                    options=[
                        {"label": 'Together', 'value':1}
                    ],
                    switch=True,
                    value=[0],
                    id=id('switch_map_displacement_together')
                )
            ]),
            dbc.Col([
                dcc.Markdown('Date range:'),
                dcc.DatePickerRange(
                    clearable=True,
                    start_date = '1993-01-01',
                    end_date = '2023-01-01',
                    min_date_allowed = '1993-01-01',
                    max_date_allowed = '2023-01-01', ## FIX: how to set dates appropriately
                    id=id('datepicker_map_displacement')
                )
            ]),
            dbc.Col([
                dcc.Markdown('Resample:'),
                dcc.Slider(
                    0, 3,
                    step = None,
                    value = 0,
                    marks = {
                        0: {'label': 'None'},
                        1: {'label': '1M'},
                        2: {'label': '6M'},
                        3: {'label': '1Y'}
                    },
                    id=id('slider_map_displacement_resample')
                )
            ]),
                       
        ],
            justify='center'
        ),
        html.Br(),
        html.Div(id=id('div_map_displacement'))
], label= "PLAN"
)


#-------------------
#    OUTER LEVEL
#-------------------
layout = dbc.Row([
    dbc.Col([
        html.Div([
            html.Br(),
            html.H1('Piazza dei Miracoli'),
            html.H4('Monitoring data analysis and visualization'),
            html.Br(),
            dbc.Tabs([
                s_tab_history,
                s_tab_plan,
            ])
        ]),
    ], lg=dict(width=10, offset=0)
    ), #dbc.Col(width=1)
])


#=================
#    CALLBACKS
#=================
#--------------------------
#    SQUARE HISTORY tab
#--------------------------
#---Gantt chart levelling
@callback(Output(id('gantt'), 'figure'),
             Input(id('checklist_gantt'), 'value'))
def callFigureGantt(which):
    return figureGantt(
        which,
        S_LEVELLING_DATA,
        PR_X,
        ERS_ASC,
        ERS_DES,
        ENV_ASC,
        SEN_ASC,
        CSK_ASC,
        
    )

#-----------------------
#    SQUARE PLAN tab
#-----------------------
#--Cheklist square map
@callback(Output(id('map_square'), 'figure'),
             Input(id('checklist_map_square'), 'value'),
             Input(id('radioitems_map_square'), 'value'),
             Input(id('rangeslider_map_square_coherence'), 'value'),
             Input(id('rangeslider_map_square_height'),'value'))

def callMapSquare(benchplot, vertical_bool, crange, hrange):
    if vertical_bool:
        return map_square_vertical(
            benchplot,
            S_LEVELLING_INFO,
            ERS_VER_INFO,
            ENV_VER_INFO,
            SEN_VER_INFO,
            CSK_VER_INFO
        )
    return map_square(
        benchplot, crange, hrange,
        S_LEVELLING_INFO,
        ERS_LOS_INFO,
        ENV_LOS_INFO,
        SEN_LOS_INFO,
        CSK_LOS_INFO
    )

#--Return number of points
## FIX: it should return the number of points AFTER filtering
@callback(Output(id('number_points_map_square'), 'children'),
            Input(id('checklist_map_square'), 'value'),
            Input(id('radioitems_map_square'), 'value'))
def callMapNumberPoints(benchplot, vertical_bool):
    if vertical_bool:
        datasets = {
            'Lev. reliable':S_LEVELLING_INFO[S_LEVELLING_INFO['rel']==1].shape[0], # benchmarks on rows
            'Lev. unreliable':S_LEVELLING_INFO[S_LEVELLING_INFO['rel']==0].shape[0], # benchmarks on rows
            'ERS':ERS_VER_INFO.shape[0],    # scatterers on rows
            'ENVISAT':ENV_VER_INFO.shape[0],    # "
            'Sentinel-1':SEN_VER_INFO.shape[0],   # "
            'COSMO-SkyMed':CSK_VER_INFO.shape[0]  # "
        }
    else:
        datasets = {
            'Lev. reliable':S_LEVELLING_INFO[S_LEVELLING_INFO['rel']==1].shape[0], # benchmarks on rows
            'Lev. unreliable':S_LEVELLING_INFO[S_LEVELLING_INFO['rel']==0].shape[0], # benchmarks on rows
            'ERS':ERS_LOS_INFO.shape[0],    # scatterers on rows
            'ENVISAT':ENV_LOS_INFO.shape[0], # "
            'Sentinel-1':SEN_LOS_INFO.shape[0],   # "
            'COSMO-SkyMed':CSK_LOS_INFO.shape[0]  # "
        }
    if benchplot == []:
        return 'Select at least one source.'
    string = ''
    for source in benchplot:
        x = datasets[source]
        string += 'Points in **' + source + '** = {} — '.format(x)

    return string[:-3]


#--Plot displacement of selected points
@callback(Output(id('div_map_displacement'), 'children'),
            Input(id('map_square'), 'selectedData'),
            Input(id('switch_map_displacement_together'), 'value'),
            Input(id('datepicker_map_displacement'), 'start_date'),
            Input(id('datepicker_map_displacement'), 'end_date'),
            Input(id('slider_map_displacement_resample'), 'value'))
def callDivMapSquare(points_from_map, together, start, end, resample_idx):
    resampler_list = [None, 'M', '6M', 'Y']
    daterange = [start, end]
    together = sum(together)
    together_list = [False, True]
    try:
        p_list = [el['customdata'] for el in points_from_map['points']]
        children = MapPointsDisplacement(
            p_list, together_list[together], daterange,
            S_LEVELLING_DATA,
            ERS_LOS_INFO,
            ERS_ASC,
            ERS_DES,
            ERS_VER_INFO,
            ERS_VER,
            ENV_LOS_INFO,
            ENV_ASC,
            ENV_DES,
            ENV_VER_INFO,
            ENV_VER,
            SEN_LOS_INFO,
            SEN_ASC,
            SEN_DES,
            SEN_VER_INFO,
            SEN_VER,
            CSK_LOS_INFO,
            CSK_ASC,
            CSK_DES,
            CSK_VER_INFO,
            CSK_VER,
            resample=resampler_list[resample_idx]
        )
    except:
        children = dcc.Markdown('Select at least one point.')
    return children
    
