# package imports
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

# local imports
from utils.utils import id_factory
id = id_factory('baptistery')
from .functions import *

# page registration
dash.register_page(
    __name__,
    path='/baptistery',
    title='Baptistery monitoring data'
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
# INFO tab
#----This tab contains info regarding the available
#----monitoring data.
b_tab_info = dbc.Tab([
    html.Br(),
    html.P(
        "This tab contains information regarding sensors installed on the Baptistery and available data.",
        style=dict(color='grey', fontSize='small')
    ),
    html.H2('Installed instrumentation'),
    html.P(
        """Availability of data from the different sources:"""
    ),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id=id('fig_gantt'),
                config=dict(
                    displayModeBar=False
                    )
            ),
            width=9,
            align='center'
        ),
        dbc.Col([
            dcc.Markdown("**Sensors to show**"),
            dbc.Checklist(
                id=id('checklist_gantt'),
                options=['Prisms', 'Levelling', 'Cracks'],
                value=['Prisms', 'Levelling', 'Cracks'],
                inline=False
            )
        ],
            width=3,
            align='center'
        ),
    ],
        justify='center'
    ),
    html.H3('Sensors and sensitivity'),
    dcc.Markdown(
        [
            """
            a) Topographical survey with prisms and [**LEICA TS503 total station**](https://rentals.leica-geosystems.com/support/F90DBE44-5056-8236-9A2DC0E9FDFA0DD1.pdf):

                - angular precision of ± 0.15 mgon, ± 0.20 mm @ 100 m;
                - linear precision of ± 0.60 mm, + 1.00 ppm @ 100 m;
                - experimentally determined errors within ± 0.30 mm @ 100 m.

            b) Crack measurements with LVDTs and thermometers: *wip*.

            c) Optical levelling: *wip*.
            """
        ]
    ),
],
    label='INFO'
)


# CHECKS Tab
#----This tab will contain data checks:
b_tab_checks = dbc.Tab([
    html.Div([
        html.Br(),
        html.P("This tab contains plots to check levelling and prism measurements against each other.",
          style=dict(color='grey', fontSize='small'))
    ]),
    html.Div([
        dcc.Markdown('## Levelling data *vs* vertical component of prisms'),
        dcc.Markdown("""
        Each levelling rod has been paired with the closest prism. Prisms, however, have an average elevation of 7 m, while levelling rods are placed at about 1.6 m above the pavement.
        """)
    ] + b_divchildren_levelling_checks)
], label='CHECKS')


# PLAN Tab
#----This tab will contain plan plots.
b_tab_plan = dbc.Tab([
    html.Div([
        html.Br(),
        html.P("This tab contains plots of prisms in plan view.",
          style=dict(color='grey', fontSize='small')),
    ]),
    html.Div([
        html.H2("Plan view of prisms"),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id=id('fig_prism_plan')),
            width=9, align='center'
            ),
            dbc.Col([
                dcc.Markdown("**Date range**"),
                dcc.RangeSlider(id=id('slider_prism_plan_daterange'),
                               min=0, max=(x:=len(B_PRISMS)-1), step=1,
                               value=[0, x],
                               marks=None,
                               allowCross=False,
                               pushable=True,
                               updatemode='drag'
                ),
                dcc.Markdown(id=id('text_prism_plan_daterange')),
                html.Br(),
                dcc.Markdown('**Scaling factor**'),
                dcc.Slider(id=id('slider_prism_plan_scalefactor_log'),
                          min=0, max=3, step=1,
                          marks={i: '{}'.format(10 ** i) for i in range(4)},
                          value=3,
                          updatemode='drag'),
                dcc.Slider(id=id('slider_prism_plan_scalefactor_dec'),
                           min=0, max=10, step=1,
                           marks={i: '{}'.format(i) for i in [0, 2, 4, 6, 8, 10]},
                           value=3,
                           updatemode='drag'),
                dcc.Markdown(id=id('text_prism_plan_scalefactor')),
                html.Br(),
                dcc.Markdown('**Floor selection**'),
                dbc.Checklist(id=id('checklist_prism_plan_floor'),
                              options=['First', 'Second'],
                              value=['Second'],
                              inline=False
                             )
            ],
            width=3, align='center'
            )
        ])
    ])
], label='PLAN')


# SECTION Tab
#----This tab will contain section plots.
b_tab_section = dbc.Tab([
    html.Div([
        html.Br(),
        html.P("This tab contains plots of prisms in section view.",
          style=dict(color='grey', fontSize='small'))
    ]),
    html.Div([
        html.H2("Section view of the prisms"),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id=id('fig_prism_section')),
            width=9, align='center'
            ),
            dbc.Col([
                dcc.Markdown('**Select a section**'),
                dcc.Slider(id=id('slider_prism_section_selection'),
                          min=1, max=12, step=1,
                          value=5,
                           updatemode='drag'
                          ),
                dcc.Graph(id=id('fig_prism_section_selection'),
                         config=dict(
                         displayModeBar=False,
                     )),
                html.Br(),
                dcc.Markdown("**Date range**"),
                dcc.RangeSlider(id=id('slider_prism_section_daterange'),
                               min=0, max=(x:=len(B_PRISMS)-1), step=1,
                               value=[0, x],
                               marks=None,
                               allowCross=False,
                               pushable=True,
                               updatemode='drag'
                ),
                dcc.Markdown(id=id('text_prism_section_daterange')),
                html.Br(),
                dcc.Markdown('**Scaling factor**'),
                dcc.Slider(id=id('slider_prism_section_scalefactor_log'),
                          min=0, max=3, step=1,
                          marks={i: '{}'.format(10 ** i) for i in range(4)},
                          value=3,
                          updatemode='drag'),
                dcc.Slider(id=id('slider_prism_section_scalefactor_dec'),
                           min=0, max=10, step=1,
                           marks={i: '{}'.format(i) for i in [0, 2, 4, 6, 8, 10]},
                           value=3,
                           updatemode='drag'),
                dcc.Markdown(id=id('text_prism_section_scalefactor')),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dcc.Markdown('**Fixed base?**'),
                    ]),
                    dbc.Col([
                        dbc.Checklist(id=id('checklist_prism_section_fixedbase'),
                                  options=[{'label':'', 'value':1}],
                                  value=[1],
                                  inline=True,
                                  switch=True
                                 )
                    ])
                ])
            ],
            width=3, align='center'
            )
        ])
    ]),
    html.Br(),
    html.Div([
        html.H2('Relative displacement of selected prisms'),
        html.Div(id=id('div_relative_displacement_plots'))
    ])

], label='SECTION')


# PRISMS Tab
#----This tab will contain plots of prism displacement in time.
b_tab_prisms = dbc.Tab([
    html.Div([
        html.Br(),
        html.P("This tab contains plots of prism displacement in time.",
          style=dict(color='grey', fontSize='small'))
    ]),
    html.Div([
        html.H2("Prism displacement"),
        dcc.Markdown("""
            Select, using the pictures, the prisms for which you would like to produce displacement plots.
            Selection can be done:
            - by clicking (hold Shift or Ctrl for multiple selection);
            - using the Lasso- or Box-selection tools (on the toolbar).
        """),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id=id('fig_prism_displacement_selection'),
                  figure=b_fig_prism_selection),
            ]),
            dbc.Col([
                dbc.Checklist(
                    options = [
                        {'label': 'Together', 'value': 1}
                        ],
                    value = [0],
                    id=id('switch_prism_plot_together'),
                    switch = True
                    )
            ])
        ], align='center', justify='end')
    ]),
    html.Br(),
    html.Br(),
    html.Div(id=id('div_prism_displacement_plots')),
], label='PRISMS')


# CRACKS Tab
#----This tab contains crack plots.
b_tab_cracks = dbc.Tab([
    html.Div([
        html.Br(),
        html.P("This tab contains plots of crack width (in time) from the extensimeters.",
          style=dict(color='grey', fontSize='small'))
    ]),
    html.Div([
        html.H2('Variation of crack width'),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dcc.Markdown('**Resampling frequency**'),
                dcc.Slider(id=id('slider_crack_plots_resampling'),
                              min=0, max=3, step=1,
                              marks={0:'Hourly',
                                    1:'Daily',
                                    2:'Weekly',
                                    3:'Monthly'},
                              value=2,
                          )
            ]),
            dbc.Col([
                dcc.Markdown("""
                    Use this slider to control how dense the plots are.
                    **BEWARE**: plotting hourly data (the original dataset) takes a loooooong time!
                """)
            ])
        ], align='center')
    ]),
    html.Br(),
    html.Div(id=id('div_crack_plots'))
], label='CRACKS')

# 3D Tab
#----This tab will contain 3D plot of the prisms system.
b_tab_3D = dbc.Tab([
    html.Div([
        html.Br(),
        html.P("This tab contains plots of prisms in 3D.",
          style=dict(color='grey', fontSize='small')),
    ]),
    html.Div([
        html.H2("3D of prisms"),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id=id('fig_prism_3d')),
            width=9, align='center'
            ),
            dbc.Col([
                dcc.Markdown("**Date range**"),
                dcc.RangeSlider(id=id('slider_prism_3d_daterange'),
                               min=0, max=(x:=len(B_PRISMS)-1), step=1,
                               value=[0, x],
                               marks=None,
                               allowCross=False,
                               pushable=True,
                               updatemode='drag'
                ),
                dcc.Markdown(id=id('text_prism_3d_daterange')),
                html.Br(),
                dcc.Markdown('**Scaling factor**'),
                dcc.Slider(id=id('slider_prism_3d_scalefactor_log'),
                          min=0, max=3, step=1,
                          marks={i: '{}'.format(10 ** i) for i in range(4)},
                          value=3,
                          updatemode='drag'),
                dcc.Slider(id=id('slider_prism_3d_scalefactor_dec'),
                           min=0, max=10, step=1,
                           marks={i: '{}'.format(i) for i in [0, 2, 4, 6, 8, 10]},
                           value=3,
                           updatemode='drag'),
                dcc.Markdown(id=id('text_prism_3d_scalefactor')),
                html.Br(),
                dcc.Markdown('** Zero Floor included?**'),
                dbc.Checklist(id=id('checklist_prism_3d_floor'),
                               options=[{'label':'', 'value':1}],
                                  value=[1],
                                  inline=True,
                                  switch=True,
                                  )
            ],
            width=3, align='center'
            )
        ])
    ])
], label='3D')

#-------------------
#    OUTER LEVEL
#-------------------
layout = dbc.Row([
    dbc.Col([
        html.Div([
            html.Br(),
            html.H1('Pisa Baptistery'),
            html.H4('Monitoring data analysis and visualization'),
            html.Br(),
            dbc.Tabs([
                b_tab_info,
                b_tab_checks,
                b_tab_plan,
                b_tab_section,
                b_tab_prisms,
                b_tab_cracks,
                b_tab_3D
            ])
        ]),
    ], lg=dict(width=10, offset=0)
    ), #dbc.Col(width=1)
])



#=================
#    CALLBACKS
#=================
#----------------
#    INFO tab
#----------------
#----Gantt chart
@callback(
    Output(id('fig_gantt'), 'figure'),
    Input(id('checklist_gantt'), 'value')
)
def callFigureGantt(which):
    return figureGantt(which)



#-----------------
#     PLAN tab
#-----------------
#---Update daterange text in settings pane
@callback(Output(id('text_prism_plan_daterange'), 'children'),
             Input(id('slider_prism_plan_daterange'), 'value'))
def callTextPrismPlanDaterange(daterange):
    start = str(B_PRISMS.index[daterange[0]])
    end = str(B_PRISMS.index[daterange[1]])
    text = "From  " + start[:10] + "  to  " + end[:10]
    return text

#---Update scalefactor text in settings pane
@callback(Output(id('text_prism_plan_scalefactor'), 'children'),
             Input(id('slider_prism_plan_scalefactor_log'), 'value'),
             Input(id('slider_prism_plan_scalefactor_dec'), 'value'))
def callTextPrismPlanScalefactor(exp, factor):
    s = scaleFactorCalc(exp, factor)
    return "Displacement scale factor = {}".format(s)

#---Update prism plan plot
@callback(Output(id('fig_prism_plan'), 'figure'),
             Input(id('slider_prism_plan_daterange'), 'value'),
             Input(id('slider_prism_plan_scalefactor_log'), 'value'),
             Input(id('slider_prism_plan_scalefactor_dec'), 'value'),
             Input(id('checklist_prism_plan_floor'), 'value'))
def callFigurePrismPlan(daterange, scale_log, scale_dec, floor):
    scalefactor = scaleFactorCalc(scale_log, scale_dec)
    return figurePrismPlan(daterange, scalefactor, floor, B_PRISMS, B_PRISM_POS)


#---------------------
#    SECTION tab
#---------------------
#---Update daterange text in settings pane
@callback(Output(id('text_prism_section_daterange'), 'children'),
             Input(id('slider_prism_section_daterange'), 'value'))
def callTextPrismSectionDaterange(daterange):
    start = str(B_PRISMS.index[daterange[0]])
    end = str(B_PRISMS.index[daterange[1]])
    text = "From  " + start[:10] + "  to  " + end[:10]
    return text

#---Update scalefactor text in settings pane
@callback(Output(id('text_prism_section_scalefactor'), 'children'),
             Input(id('slider_prism_section_scalefactor_log'), 'value'),
             Input(id('slider_prism_section_scalefactor_dec'), 'value'))
def callTextPrismSectionScalefactor(exp, factor):
    s = scaleFactorCalc(exp, factor)
    return "Displacement scale factor = {}".format(s)

#--Update section selection plot
@callback(Output(id('fig_prism_section_selection'), 'figure'),
             Input(id('slider_prism_section_selection'), 'value'))
def callFigurePrismSectionSelection(selection):
    p = str(selection)
    if len(p) == 1:
        p = '0' + p
    selected_prisms = selectPrismSection(p)
    return figureSectionSelection(selected_prisms, B_PRISM_POS)

#---Update prism section plot
@callback(Output(id('fig_prism_section'), 'figure'),
             Input(id('slider_prism_section_selection'), 'value'),
             Input(id('slider_prism_section_daterange'), 'value'),
             Input(id('slider_prism_section_scalefactor_log'), 'value'),
             Input(id('slider_prism_section_scalefactor_dec'), 'value'),
             Input(id('checklist_prism_section_fixedbase'), 'value'))
def callFigurePrismSection(selection, daterange, scale_log, scale_dec, fixedbase):
    s = scaleFactorCalc(scale_log, scale_dec)
    if len(fixedbase) == 1:
        f = True
    else:
        f = False
    p = str(selection)
    if len(p) == 1:
        p = '0' + p
    selected_prisms = selectPrismSection(p)
    return figurePrismSection(selected_prisms, daterange, s, f, B_PRISMS)

#---Plot relative displacements
@callback(Output(id('div_relative_displacement_plots'), 'children'),
             Input(id('slider_prism_section_selection'), 'value'))
def callFigureRelativeDisplacements(selection):
    p = str(selection)
    if len(p) == 1:
        p = '0' + p
    selected_prisms = selectPrismSection(p)
    selected_prisms.sort()
    links = [
        [0,1], [2,3], [4,5], [6,7],
        [0,2], [1,3], [4,6], [5,7]
    ]
    couples = [[selected_prisms[l[0]], selected_prisms[l[1]]] for l in links]

    children = []
    for c in couples:
        row = dbc.Row([
            dbc.Col([dcc.Graph(figure=figureSectionRelativeDisplacements(c, B_PRISMS, B_EXTENSIMETERS))], width=9),
            dbc.Col([dcc.Graph(figure=figurePrismCoupleSelection(c, B_PRISM_POS))], width=3)
        ], align='center')
        children.append(row)

    return children


#------------------
#    PRISMS tab
#------------------
#---Select prisms and plot their displacement
@callback(Output(id('div_prism_displacement_plots'), 'children'),
             Input(id('fig_prism_displacement_selection'), 'selectedData'),
             Input(id('switch_prism_plot_together'), 'value'))
def callDivPrismDisplacement(selectedData, together_switch):
    try:
        if sum(together_switch) == 1:
            prisms = [el['customdata'] for el in selectedData['points']]
            children = [dcc.Graph(figure=figurePrismDisplacementTogether(prisms, c, B_PRISMS, B_EXTENSIMETERS)) for c in ['Total', 'Radial', 'Vertical', 'Tangential']]
        else:
            prisms = [el['customdata'] for el in selectedData['points']]
            children = [dcc.Markdown('''
                In each plot, you can select which traces to exclude or include by clicking on their legend entries. You can isolate a trace by double-clicking it.
            ''')]
            children += [dcc.Graph(figure=figurePrismDisplacement(p, B_PRISMS, B_EXTENSIMETERS)) for p in prisms]
    except:
        children = dcc.Markdown('Select at least one prism.')
    return children


#---------------------
#    CRACKS tab
#---------------------
#---Select resampling frequency and update plots
@callback(Output(id('div_crack_plots'), 'children'),
             Input(id('slider_crack_plots_resampling'), 'value'))
def callDivCrackPlots(res_val):
    res_freqs = ['H', 'D', 'W', 'M']
    freq = res_freqs[res_val]
    children = []
    for i,e in enumerate(['F3CE', 'F3CF', 'F3D1', 'F3D2', 'F46C', 'F46D', 'F3D0', 'F46B']):
        row = dbc.Row([
            dbc.Col([
                    dcc.Graph(figure=figureExtensimeter(e, B_EXTENSIMETERS, resampling=freq))
                        ], width={"size": 9}),
            dbc.Col([
                dcc.Graph(figure=b_extensimeter_positions[i], config=dict(
                         displayModeBar=False,
                     ))
            ], width={"size": 3})
        ], align='center')
        children.append(row)
    return children

#------------
# 3D tab
#------------
#---Update daterange text in settings pane
@callback(Output(id('text_prism_3d_daterange'), 'children'),
             Input(id('slider_prism_3d_daterange'), 'value'))
def callTextPrism3dDaterange(daterange):
    start = str(B_PRISMS.index[daterange[0]])
    end = str(B_PRISMS.index[daterange[1]])
    text = "From  " + start[:10] + "  to  " + end[:10] 
    return text

#---Update scalefactor text in settings pane
@callback(Output(id('text_prism_3d_scalefactor'), 'children'),
             Input(id('slider_prism_3d_scalefactor_log'), 'value'),
             Input(id('slider_prism_3d_scalefactor_dec'), 'value'))
def callTextPrism3dScalefactor(exp, factor):
    s = scaleFactorCalc(exp, factor)
    return "Displacement scale factor = {}".format(s)

#---Update prism 3d plot
@callback(Output(id('fig_prism_3d'), 'figure'),
             Input(id('slider_prism_3d_daterange'), 'value'),
             Input(id('slider_prism_3d_scalefactor_log'), 'value'),
             Input(id('slider_prism_3d_scalefactor_dec'), 'value'),
             Input(id('checklist_prism_3d_floor'), 'value'))
def callFigurePrism3d(daterange, scale_log, scale_dec, zero_floor):
    scalefactor = scaleFactorCalc(scale_log, scale_dec)
    return figurePrism3d(B_PRISMS,daterange, scalefactor, zero_floor,CONNMAT)
    
    
    
