# imports
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import dcc

# local imports
from utils.styles import *


#==============================
#    TAB-SPECIFIC FUNCTIONS
#==============================
#--------------------------
#    SQUARE HISTORY TAB
#--------------------------
def figureGantt(
    which,
    disp_square,
    ERS_asc_disp,
    ERS_desc_disp,
    ENV_asc_disp,
    S_asc_disp,
    C_asc_disp,
    ):
    """
    Plots a Gantt chart with the temporal availability of data.
    Expects:
    - which = list of instrumentation to plot.
    - dataframes with monitoring data
    Returns:
    - figure object
    """
    ERS_disp=pd.concat([ERS_asc_disp,ERS_desc_disp])
    #lev_tot=pd.concat([lev_tower,DF_disp],axis=1)
    which_df = {
        'Square levelling': disp_square,
        'ERS': ERS_disp,
        'ENVISAT': ENV_asc_disp,
        'Sentinel-1': S_asc_disp,
        'COSMO-SkyMed': C_asc_disp,
    }

    fig = go.Figure(layout_template=None)
    for i, w in enumerate(which):
        df = which_df[w]
        ind=df.sort_index().index
        my_index = ind
        fig.add_trace(
            go.Scatter(x=my_index, y=[w]*len(my_index),
                   mode='markers', name=w,
                      marker_color=colors[i],
                      marker_size = 10,
                      marker_symbol='square')
        )

    fig.update_layout(dict(yaxis_range=(-0.5, len(which)-0.5)),
                     margin=dict(l=100,r=20, t=20))
    fig.update_layout(dict(showlegend=False))
    fig.update_layout(hovermode='x unified')
    fig.update_traces(hovertemplate="%{x}")
    return fig


#-----------------------
#    SQUARE PLAN TAB
#-----------------------
def map_square_vertical(
    benchplot, pos_square,
    ERS_vcoord, ENV_vcoord,
    S_vcoord, C_vcoord):
    '''
    An open-street-map figure with reliable
    (and unreliable) benchmarks and satellite
    points (VERTICAL DISPLACEMENTS ONLY)
    '''
    ## FIX: colors
    fig=go.Figure()
    if len(benchplot)<1:
        d={'lat':[0],'lon':[0]}
        blank_map=pd.DataFrame(data=d)

        fig.add_trace(go.Scattermapbox(lat=blank_map["lat"], lon=blank_map["lon"]))

    if 'Lev. reliable' in benchplot:
        fig.add_trace(
            go.Scattermapbox(
                lat=pos_square[pos_square['rel']==1]["lat"],
                lon=pos_square[pos_square['rel']==1]["lon"],
                marker=go.scattermapbox.Marker(
                    size=7,
                    color='#332288',
                    opacity=1
                ),
                text=[n for n in pos_square[pos_square['rel']==1].index] ,
                customdata=[n for n in pos_square[pos_square['rel']==1].index],
                hoverinfo='text',
                name='Levelling reliable'
            )
        )

    if 'Lev. unreliable' in benchplot:
        fig.add_trace(
            go.Scattermapbox(
                lat=pos_square[pos_square['rel']==0]["lat"],
                lon=pos_square[pos_square['rel']==0]["lon"],
                marker=go.scattermapbox.Marker(
                    size=7,
                    color='#EE3377',
                    opacity=1,),
                text=[n for n in pos_square[pos_square['rel']==0].index],
                customdata=[n for n in pos_square[pos_square['rel']==0].index],
                hoverinfo='text',
                name='Levelling unreliable'
            )
        )

    if 'ERS' in benchplot:
        fig.add_trace(
            go.Scattermapbox(
                lat=ERS_vcoord["LAT"],
                lon=ERS_vcoord["LON"],
                marker=go.scattermapbox.Marker(
                    size=7,
                    color='#117733',
                    opacity=1,),
                text=[n for n in ERS_vcoord.index],
                hoverinfo='text',
                customdata=[n for n in ERS_vcoord.index],
                name='ERS'
            )
        )

    if 'ENVISAT' in benchplot:
        fig.add_trace(
            go.Scattermapbox(
                lat=ENV_vcoord["LAT"],
                lon=ENV_vcoord["LON"],
                marker=go.scattermapbox.Marker(
                    size=7,
                    color='#44AA99',
                    opacity=1,),
                text=[n for n in ENV_vcoord.index],
                hoverinfo='text',
                customdata=[n for n in ENV_vcoord.index],
                name='ENVISAT'
            )
        )


    if 'COSMO-SkyMed' in benchplot:
        fig.add_trace(
            go.Scattermapbox(
                lat=C_vcoord["LAT"],
                lon=C_vcoord["LON"],
                marker=go.scattermapbox.Marker(
                    size=7,
                    color='#CC6677',
                    opacity=1,),
                text=[n for n in C_vcoord.index],
                hoverinfo='text',
                customdata=[n for n in C_vcoord.index],
                name='COSMO-SkyMed'
            )
        )


    if 'Sentinel-1' in benchplot:
        fig.add_trace(
            go.Scattermapbox(
                lat=S_vcoord["LAT"],
                lon=S_vcoord["LON"],
                marker=go.scattermapbox.Marker(
                    size=7,
                    color='#CC3311',
                    opacity=1,),
                text=[n for n in S_vcoord.index],
                hoverinfo='text',
                customdata=[n for n in S_vcoord.index],
                name='Sentinel-1'
            )
        )

    # legend
    fig.update_layout(showlegend=True)
    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    # mapbox style
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            center=go.layout.mapbox.Center(
                lat=43.7231,
                lon=10.396
            ),
            pitch=0,
            zoom=16.3,
        ),
        clickmode='event+select'
    )

    return fig


def map_square(
    benchplot, crange, hrange,
    pos_square,
    ERS_coord,
    ENV_coord,
    S_coord,
    C_coord
    ):
    '''
    An open-street-map figure with reliable (and unreliable)
    benchmarks and satellite points.
    '''

    fig=go.Figure()

    ## FIX:colors
    datasets = {
        'ERS': [ERS_coord, ['#117733', '#999933']],
        'ENVISAT': [ENV_coord, ['#44AA99', '#88CCEE']],
        'COSMO-SkyMed': [C_coord, ['#CC6677', '#DDCC77']],
        'Sentinel-1': [S_coord, ['#CC3311', '#EE7733']]
    }

    # In case NO data sources are selected
    if len(benchplot)<1:
        d={'lat':[0],'lon':[0]}
        blank_map=pd.DataFrame(data=d)
        fig.add_trace(go.Scattermapbox(lat=blank_map['lat'], lon=blank_map['lon']))

    for b in benchplot:
        if b == 'Lev. reliable':
            fig.add_trace(
                go.Scattermapbox(
                    lat=pos_square[pos_square['rel']==1]["lat"],
                    lon=pos_square[pos_square['rel']==1]["lon"],
                    marker=go.scattermapbox.Marker(
                        size=7,
                        color='#332288',
                        opacity=1,),
                    text=[n for n in pos_square[pos_square['rel']==1].index] ,
                    customdata=[n for n in pos_square[pos_square['rel']==1].index],
                    hoverinfo='text',
                    name='Levelling reliable'
                )
            )

        elif b == 'Lev. unreliable':
            fig.add_trace(
                go.Scattermapbox(
                    lat=pos_square[pos_square['rel']==0]["lat"],
                    lon=pos_square[pos_square['rel']==0]["lon"],
                    marker=go.scattermapbox.Marker(
                        size=7,
                        color='#EE3377',
                        opacity=1,),
                    text=[n for n in pos_square[pos_square['rel']==0].index],
                    customdata=[n for n in pos_square[pos_square['rel']==0].index],
                    hoverinfo='text',
                    name='Levelling unreliable'
                )
            )

        else:
            d = datasets[b][0]
            d = d[d['COHER'] >= crange[0]]
            d = d[d['COHER'] <= crange[1]]
            d = d[d['HEIGHT'] >= hrange[0]]
            d = d[d['HEIGHT'] <= hrange[1]]
            cols = datasets[b][1]

            fig.add_trace(
                go.Scattermapbox(
                    lat=d[d['TYPE']=='asc']['LAT'],
                    lon=d[d['TYPE']=='asc']['LON'],
                    marker=go.scattermapbox.Marker(
                        size=7,
                        color=cols[0],
                        opacity=1),
                    text=[n for n in d[d['TYPE']=='asc'].index],
                    hoverinfo='text',
                    customdata=[n for n in d[d['TYPE'] == 'asc'].index],
                    name=b+' ascending'
                )
            )
            fig.add_trace(
                go.Scattermapbox(
                    lat=d[d['TYPE']=='des']['LAT'],
                    lon=d[d['TYPE']=='des']['LON'],
                    marker=go.scattermapbox.Marker(
                        size=7,
                        color=cols[1],
                        opacity=1),
                    text=[n for n in d[d['TYPE']=='des'].index],
                    hoverinfo='text',
                    customdata=[n for n in d[d['TYPE'] == 'des'].index],
                    name=b+' descending'
                )
            )

    fig.update_layout(showlegend=True)
    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            center=go.layout.mapbox.Center(
                lat=43.7231,
                lon=10.396
            ),
            pitch=0,
            zoom=16.3,
        ),
        clickmode='event+select'
    )

    return fig


def MapPointsDisplacement(p_list, together, daterange,
                          disp_square,
                          ERS_coord,
                          ERS_asc_disp,
                          ERS_desc_disp,
                          ERS_vcoord,
                          ERS_vdisp,
                          ENV_coord,
                          ENV_asc_disp,
                          ENV_desc_disp,
                          ENV_vcoord,
                          ENV_vdisp,
                          S_coord,
                          S_asc_disp,
                          S_desc_disp,
                          S_vcoord,
                          S_vdisp,
                          C_coord,
                          C_asc_disp,
                          C_desc_disp,
                          C_vcoord,
                          C_vdisp,
                          resample=None):
    ## FIX: colors
    # Levelling dataset
    disp_square=disp_square*1000 #mm
    for col in disp_square.columns:
        disp_square[col] = (disp_square[col] - disp_square.loc[disp_square[col].first_valid_index(), col])
    levelling = disp_square

    # Satellite datasets
    # [dataset, color, resamplable, h+coher, coordinate dataset]
    datasets = {
        'ers-a': [ERS_asc_disp, '#117733', False, True, ERS_coord],
        'ers-d': [ERS_desc_disp, '#999933', False, True, ERS_coord],
        'ers-v': [ERS_vdisp, '#117733', False, False, ERS_vcoord],
        'env-a': [ENV_asc_disp, '#44AA99', False, True, ENV_coord],
        'env-d': [ENV_desc_disp, '#88CCEE', False, True, ENV_coord],
        'env-v': [ENV_vdisp, '#44AA99', False, False, ENV_vcoord],
        'sen-a': [S_asc_disp, '#CC3311', True, True, S_coord],
        'sen-d': [S_desc_disp, '#EE7733', True, True, S_coord],
        'sen-v': [S_vdisp, '#CC3311', True, False, S_vcoord],
        'csk-a': [C_asc_disp, '#CC6677', True, True, C_coord],
        'csk-d': [C_desc_disp, '#DDCC77', True, True, C_coord],
        'csk-v': [C_vdisp, '#CC6677', True, False, C_vcoord],

    }

    # SWITCH: *together* means all plots in the same figure,
    # otherwise separate figures. In either case, the function
    # returns a list of figures (with just one element if *together*=True).
    # There is only ONE plotting function. To send the plotly Trace
    # to the right plotly Figure object, we use a list of indices
    # to be iterated over at the same time as *p_list*. This list
    # of indices, called *figs_indices*, is made up of all ZEROS if *together*=True,
    # so that all plotly Traces are sent to the one and only Figure in
    # the *figs* list. Otherwise, it's just a range with the same
    # length as *p_list*.
    if together:
        figs = [
            go.Figure(layout_template='plotly_white')
        ]
        figs_indices = [0]*len(p_list)

    else:
        figs = []
        for k in p_list:
            figs.append(go.Figure(layout_template='plotly_white'))
        figs_indices = range(len(p_list))

    for idx_figure, p in zip(figs_indices, p_list):
        try:
            d = datasets[p[:5]] # If the point is a PS
            if resample != None and d[2]:
                d[0] = d[0].resample(resample).mean()
        except:
            d = [levelling, '#332288', False, False]

        data=d[0].loc[daterange[0]:daterange[1]]
        figs[idx_figure].add_trace(
            go.Scatter(
                x=data.index,
                y=data[p],
                mode='markers+lines',
                marker_color = d[1],
                line_color = d[1],
                name=str(p)
                )
        )
        figs[idx_figure].update_layout(
            yaxis_title="Displacement [mm]",
        )

        # Write name and, if relevant, coherence and height
        if d[3] and not together:
            figs[idx_figure].update_layout(
                title={
                    'text': "<b>{}</b>   Height = {} m, Coherence = {}".format(p, d[4].loc[p]['HEIGHT'], d[4].loc[p]['COHER']),
                    'yref':"container",
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font_color':'black',
                    'font_size': 14
                }
            )
        elif not together:
            figs[idx_figure].update_layout(
                title={
                    'text': "<b>{}</b>".format(p),
                    'yref':"container",
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font_color':'black',
                    'font_size': 14
                }
            )

    children = [dcc.Graph(id='tmp_graph{}'.format(idx_f), figure=f) for idx_f, f in enumerate(figs)]
    return children



