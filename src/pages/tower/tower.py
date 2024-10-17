# package imports
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

# local imports
from utils.utils import id_factory
id = id_factory('tower')
from .functions import *
from data.tower_data import *

# page registration
dash.register_page(
    __name__,
    path='/tower',
    title='Monitoring data of the Leaning Tower of Pisa'
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
# TOWER PLAN Tab
#----In this tab you can plot the displacements of benchmarks
#----in the Tower and in the Catino, choosing from a plan view

# standalone figures
## FIX: these two functions are practically the same: unify them
t_fig_bench_sel = figureBenchSelection(T_CAPRARO_BENCHMARKS)
t_fig_stabil_bench_sel = figureBenchStabilSelection(T_STABIL_COORDS)

# tab itself
t_tab_plan= dbc.Tab([
    html.Div([
        html.Br(),
        html.P("This tab contains plots of levelling measurement of the tower",
          style=dict(color='grey', fontSize='small'))
    ]),
    html.Div([
        html.H2('Plan view of the benchmarks'),
        dcc.Markdown(
            """
            Select, using the pictures, the prisms for which you would like to produce displacement plots.
            Selection can be done:
            - by clicking (hold Shift or Ctrl for multiple selection);
            - using the Lasso- or Box-selection tools (on the toolbar).
            """
        ),
        html.Br(),
        dcc.Markdown("Circle benchmarks are also part of the altimetric monitoring of the square, unlike the diamond-shaped ones."),
    ]),
    html.Div([
            dbc.Row([
                dbc.Col([
                    dcc.Markdown('**Levelling during 2002-2022:**',),
                    dcc.Graph(id=id('fig_bench_displacement_selection'), figure=t_fig_bench_sel),
                    
                ],
                    width=6, align='left'
                ),
                dbc.Col([
                    dcc.Markdown('**Levelling during soil freezing and application of lead weights (1995-1999):**'),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(id=id('fig_stabil_bench_displacement_selection'), 
                    figure=t_fig_stabil_bench_sel),
                ],
                    width=6, align='right'
                ),
            ]),
    ]),
    html.Br(),
    html.Div(id=id('div_bench_displacement_plots')),
    html.Button("Download CSV", id="btn-download"),
    dcc.Download(id="download-data"),
    html.Br(),
    html.Div(id=id('div_stabil_bench_displacement_plots')),
],
    label='LEVELLING PLAN'
)


# TOWER SECTION Tab
#----In this tab you can plot the displacements of benchmarks
#----in the Tower and in the Catino, as seen in section view

# standalone figures
t_rot_tower = rot_tower(T_CAPRARO_DATA)

# the tab itself
t_tab_section = dbc.Tab([
    html.Div([
        html.Br(),
        html.P(
            "This tab contains plots of benchmarks in section view.",
            style=dict(color='grey', fontSize='small')
        )
    ]),
    html.Div([
        html.H2("Section view of the benchmarks"),
        dcc.Markdown(
            """
            Select, using the slider on the side, the section whose displacements you want to see. \n
            A resampling of the data can be done with the slider immediately below.
            """
        ),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id=id('fig_bench_section')),
            ],
                width=9, align='center'
            ),
            dbc.Col([
                dcc.Markdown('**Select a section**'),
                dcc.Slider(
                    id=id('slider_bench_section_selection'),
                    min=1, max=4, step=1,
                    value=1,
                    updatemode='drag'
                ),
                dcc.Graph(
                    id=id('fig_bench_section_selection'),
                    config=dict(
                        displayModeBar=False,
                    )
                ),
                html.Br(),
                dcc.Markdown("**Resampling of data**"),
                dcc.Slider(
                    id=id('slider_bench_section_resample'),
                    min=0, max=6, step=1,
                    value=6,
                    marks={
                        0: 'M',
                        1: '2M',
                        2: '4M',
                        3: '6M',
                        4: '8M',
                        5: '10M',
                        6: '12M'
                    },
       
                    updatemode='drag'
                ),
                dcc.Markdown(id=id('text_bench_section_resample')),
            ], 
                width=3, align='top'
            )
        ])
    ]),
    html.Div(id=id('div_rot'))
],
    label='LEVELLING SECTIONS'
)


# TOWER STATIC MONITORING Tab
#----In this tab you can plot and export data from static
#----monitoring of the Tower

# accordion for sensor selection
from data.tower.static_sensor_list import t_sensor_dict


# the tab itself
t_tab_static= dbc.Tab([
    html.Div([
        html.Br(),
        html.P("This tab is for plotting and exporting static monitoring data of the Tower.",
          style=dict(color='grey', fontSize='small'))
    ]),
    html.Div([
        html.H2('Static monitoring data'),
        
            ],
        ),
        
    html.Div([
        html.Iframe(
        src="http://www.maxmartino.it/torre/index.htm",  # Link al sito da includere
        style={"width": "80%", "height": "450px", "border": "none"}  # Dimensioni e stile dell'iframe
       
        ),
        
            ],
        ),
    html.Br(), html.Br(), html.Br(),  # Blank space  
    html.Div([
     dbc.Row([
    dbc.Col([
    dcc.Markdown("**Select or write sensor names**"),
    dcc.Dropdown(
        id='dropdown-telecoordinometers',
        options=[{'label': item, 'value': item} for item in t_sensor_dict['telecoordinometers']],
        multi=True,
        placeholder='Select Telecoordinometers',
        style={'width': '300px'}
    ),
    dcc.Dropdown(
        id='dropdown-GB_pendulum',
        options=[{'label': item, 'value': item} for item in t_sensor_dict['GB_pendulum']],
        multi=True,
        placeholder='Select GB pendulum',
        style={'width': '300px'}
    ),
    dcc.Dropdown(
        id='dropdown-inclinometers',
        options=[{'label': item, 'value': item} for item in t_sensor_dict['inclinometers']],
        multi=True,
        placeholder='Select Inclinometers',
        style={'width': '300px'}
    ),
    dcc.Dropdown(
        id='dropdown-inc_temp',
        options=[{'label': item, 'value': item} for item in t_sensor_dict['inclinometers_temp']],
        multi=True,
        placeholder='Select Inclinometers temperature',
        style={'width': '300px'}
    ),
    dcc.Dropdown(
        id='dropdown-deformometers',
        options=[{'label': item, 'value': item} for item in t_sensor_dict['deformometers']],
        multi=True,
        placeholder='Select Deformometers',
        style={'width': '300px'}
    ),
    dcc.Dropdown(
        id='dropdown-temp',
        options=[{'label': item, 'value': item} for item in t_sensor_dict['thermometers']],
        multi=True,
        placeholder='Select Thermometers',
        style={'width': '300px'}
    ),
   
     html.Br(),

    # Generic written input
    dcc.Input(
        id='static_input',
        type='text',
        placeholder='Add sensor names separeted by commas',
        style={'width': '300px'}
    ),
    html.Br(),
], width=3, align='left' ),

    dbc.Col([
    html.Br(),
    html.Br(),
     dcc.Dropdown(
        id='dropdown-levellometers',
        options=[{'label': item, 'value': item} for item in t_sensor_dict['levellometers']],
        multi=True,
        placeholder='Select Levellometers',
        style={'width': '300px'}
    ),
    dcc.Dropdown(
        id='dropdown-level_temp',
        options=[{'label': item, 'value': item} for item in t_sensor_dict['levellometers_temp']],
        multi=True,
        placeholder='Select Levellometers temperature',
        style={'width': '300px'}
    ),
    dcc.Dropdown(
        id='dropdown-extensometers',
        options=[{'label': item, 'value': item} for item in t_sensor_dict['extensometers']],
        multi=True,
        placeholder='Select Wire Extensometers',
        style={'width': '300px'}
    ),
    dcc.Dropdown(
        id='dropdown-weather',
        options=[{'label': item, 'value': item} for item in t_sensor_dict['weather_station']],
        multi=True,
        placeholder='Select Weather station',
        style={'width': '300px'}
    ),
    dcc.Dropdown(
        id='dropdown-piezo',
        options=[{'label': item, 'value': item} for item in t_sensor_dict['piezometers']],
        multi=True,
        placeholder='Select Piezometers',
        style={'width': '300px'}
    ),
    dcc.Dropdown(
        id='dropdown-piezo_temp',
        options=[{'label': item, 'value': item} for item in t_sensor_dict['piezometers_temp']],
        multi=True,
        placeholder='Select Piezometers temperature',
        style={'width': '300px'}
    ),
    ], width=3, align='left' ),
   
    dbc.Col([
    dcc.Markdown('**Resample**'),
    dcc.RadioItems(
    id=id('resample_static_radio'),
    options=[
        {'label': 'Hourly', 'value': 'hourly'},
        {'label': 'Daily', 'value': 'daily'},
        {'label': 'Weekly', 'value': 'weekly'},
        {'label': 'Monthly', 'value': 'monthly'}
    ],
    value='weekly',  # Valore di default
    style={'width': '300px'}
),

], width=2, align='left' ),
    dbc.Col([
    dcc.Markdown("**Date range**"),
    dcc.DatePickerRange(
                    clearable=True,
                    start_date = '2023-02-03',
                    end_date = '2023-04-19',
                    min_date_allowed = '1993-01-01',
                    max_date_allowed = '2024-09-01', ## FIX: how to set dates appropriately
                    id=id('datepicker_static_displacement')
                ),
    html.Br(),            
    html.Br(),
    dcc.Markdown("**Together?**"),
    dbc.Checklist(options = [
                  {'label': 'Together', 'value': 1}
                        ],
                  value = [0],
                  id=id('switch_static_plot_together'),
                  switch = True
                 ),
    html.Br(),
    dcc.Markdown("**Two axes?**"),
    dbc.Checklist(options = [
                  {'label': 'Two Y axes', 'value': 1}
                        ],
                  value = [0],
                  id=id('switch_static_plot_y'),
                  switch = True
                 ),
    html.Br(),
    dcc.Markdown("**Remove outliers?**"),
    dbc.Checklist(options = [
                  {'label': 'Remove', 'value': 1}
                        ],
                  value = [0],
                  id=id('switch_static_plot_outliers'),
                  switch = True
                 ),
                

 ], width=4, align='left' ),  

]),
]),
    html.Br(),
    html.Br(),
    html.Div(id=id('div_static_displacement_plots')),
],
    label='STATIC MONITORING'
)
# TOWER STATIC INFO tab
#----In this tab you can plot the GANTT of static sensors

# tab itself
t_tab_static_info= dbc.Tab([
    html.Div([
        html.Br(),
        html.P("This tab contains GANTT of Tower'static sensors",
          style=dict(color='grey', fontSize='small'))
    ]),
    html.Div([
        html.H2('GANTT'),
        html.Br(),  
    ]),
    html.Div([ dcc.Graph(id=id('fig_static_gantt'), figure=gantt_chart()),
           
            ]),
    
  
],
    label='STATIC INFO'
)

#-------------------
#    OUTER LEVEL
#-------------------
layout = dbc.Row([
    dbc.Col([
        html.Div([
            html.Br(),
            html.H1('Leaning Tower of Pisa'),
            html.H4('Monitoring data analysis and visualization'),
            html.Br(),
            dbc.Tabs([
                t_tab_plan,
                t_tab_section,
                t_tab_static_info,
                t_tab_static
                
            ])
        ]),
    ], lg=dict(width=10, offset=0)
    ), #dbc.Col(width=1)
])

#=================
#    CALLBACKS
#=================
#----------------------
#    TOWER PLAN tab
#----------------------
#---Select Capraro benchmarks and plot their displacement
@callback(Output(id('div_bench_displacement_plots'), 'children'),
             Input(id('fig_bench_displacement_selection'), 'selectedData'))
def callDivBenchDisplacement(selectedData):
    try:
        bench = [el['customdata'] for el in selectedData['points']]
        children=[]
        children += [dcc.Graph(figure=figureBenchDisplacement(bench, T_CAPRARO_DATA))]
    except:
        children = dcc.Markdown('Select at least one benchmark.')
        
    return children
    
    
#TEST!
# Download data as a test for this graph but I can implement this button for everything
@callback(
    Output("download-data", "data"),
    Input("btn-download", "n_clicks"),
    State(id('fig_bench_displacement_selection'), 'selectedData'),
    prevent_initial_call=True
)
def download_csv(n_clicks, selectedData):
    if selectedData is None:
        return dash.no_update

    try:
        # Estrai i nomi delle colonne da selectedData
        bench = [el['customdata'] for el in selectedData['points']]
        
        # Verifica che i nomi delle colonne siano nel DataFrame
        valid_columns = [col for col in bench if col in T_CAPRARO_DATA.columns]
        
        if not valid_columns:
            return dash.no_update
        
        # Estrai i dati delle colonne valide
        df = T_CAPRARO_DATA[valid_columns]
        
        # Converti in CSV
        csv_string = df.to_csv(index=False)
        return dict(content=csv_string, filename="data.csv")
    except Exception as e:
        print(f"Errore: {e}")
        return dash.no_update

#---Select stabilization benchmarks and plot their displacement
@callback(Output(id('div_stabil_bench_displacement_plots'), 'children'),
             Input(id('fig_stabil_bench_displacement_selection'), 'selectedData'))
def callDivDFBenchDisplacement(selectedData):
    try:
        bench = [el['customdata'] for el in selectedData['points']]
        children=[]
        children += [dcc.Graph(figure=figureBenchDisplacement(bench, T_STABIL_DISP))]
    except:
        children = dcc.Markdown('')
        
    return children
    
    
#-------------------------
#    TOWER SECTION tab
#-------------------------
#----Update section selection plot
@callback(Output(id('fig_bench_section_selection'), 'figure'),
             Input(id('slider_bench_section_selection'), 'value'))
def callFigureBenchSectionSelection(selection):
    b = str(selection)
    if len(b) == 1:
        b = '0' + b    
    selected_bench = selectBenchSection(b)
    return figureSectionSel(selected_bench, T_CAPRARO_BENCHMARKS)

#----Update resample text in settings pane
@callback(Output(id('text_bench_section_resample'), 'children'),
             Input(id('slider_bench_section_resample'), 'value'))
def callTextBenchSectionresample(resample):
    reslisttext=['', '2', '4', '6', '8', '10', '12']
    reslist=list(enumerate(reslisttext))
    if resample==0:
        text= "Data isn't resampled"
    else:
        text = "Resampling with data every " + reslist[resample][1]+ "  months. \n **Pay attention**: when resampling, the days (and also months, for strong resampling) of measurement are not the real ones."        
    return text

#----Update bench section plot
@callback(Output(id('fig_bench_section'), 'figure'),
             Input(id('slider_bench_section_selection'), 'value'),
             Input(id('slider_bench_section_resample'), 'value'))        
def callFigureBenchSection(selection, resample):
    b = str(selection)
    if len(b) == 1:
        b = '0' + b
    selected_bench = selectBenchSection(b)
    return figureBenchSection(selected_bench, resample, T_CAPRARO_DATA, T_CAPRARO_BENCHMARKS)

#----Plot angle between benchmarks 904-911
@callback(Output(id('div_rot'), 'children'),
             Input(id('slider_bench_section_selection'), 'value'))
def callFigureRot(selection):
    b = str(selection)
    if b=='1' or b=='01':
        children = dbc.Row(dcc.Graph(figure=t_rot_tower))
        return children


#-----------------------------------
#    TOWER STATIC MONITORING tab
#-----------------------------------

@callback(
    Output(id('div_static_displacement_plots'), 'children'),
    [Input('dropdown-telecoordinometers', 'value'),
     Input('dropdown-GB_pendulum', 'value'),
     Input('dropdown-inclinometers', 'value'),
     Input('dropdown-inc_temp', 'value'),
     Input('dropdown-deformometers', 'value'),
     Input('dropdown-temp', 'value'),
     Input('dropdown-levellometers', 'value'),
     Input('dropdown-level_temp', 'value'),
     Input('dropdown-extensometers', 'value'),
     Input('dropdown-weather', 'value'),
     Input('dropdown-piezo', 'value'),
     Input('dropdown-piezo_temp', 'value'),
     Input('static_input', 'value'),
     Input(id('resample_static_radio'),'value'),
     Input(id('datepicker_static_displacement'),'start_date'),
     Input(id('datepicker_static_displacement'),'end_date'),
     Input(id('switch_static_plot_together'), 'value'),
     Input(id('switch_static_plot_y'), 'value'),
     Input(id('switch_static_plot_outliers'), 'value'),

     ]
)
def callDivStaticDisp(telecoordinometers, gb, inclinometers, inc_temp,defor,temp,level,level_temp,ext,weather,piezo,piezo_temp, gen_input,resample, start_date, end_date,tog,y,outliers):
    tog = sum(tog)
    yax=sum(y)
    outliers=sum(outliers)
    together_list = [False, True]
    y_list=[False,True]
    out_list=[False,True]
    combined_values = []
    if telecoordinometers:
        combined_values.extend(telecoordinometers)
    if gb:
        combined_values.extend(gb)
    if inclinometers:
        combined_values.extend(inclinometers)
    if inc_temp:
        combined_values.extend(inc_temp)
    if defor:
        combined_values.extend(defor)
    if temp:
        combined_values.extend(temp)
    if level:
        combined_values.extend(level)
    if level_temp:
        combined_values.extend(level_temp)
    if ext:
        combined_values.extend(ext)
    if weather:
        combined_values.extend(weather)
    if piezo:
        combined_values.extend(piezo)
    if piezo_temp:
        combined_values.extend(piezo_temp)
    if gen_input:
        additional_values = [value.strip() for value in gen_input.split(',')]
        combined_values.extend(additional_values)
    
    
    df=merge_and_filter_dataframe('data/tower/parquet_data/static/*',resample, combined_values, start_date, end_date)
    
    try:
        children = figureStaticDisplacement(df, start_date,end_date,together_list[tog],y_list[yax],out_list[outliers])
    except:
        children = dcc.Markdown('Select at least one sensor.')

    return children
