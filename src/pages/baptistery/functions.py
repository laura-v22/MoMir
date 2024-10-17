# package imports
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc


# local imports
from data.baptistery_data import B_PRISMS, B_LEVELLING, B_EXTENSIMETERS, CONNMAT
from data.baptistery_data import B_PRISM_POS, B_LEVELLING_POS, B_EXTENSIMETER_POS, B_POSITIONS
from utils.styles import *
from utils.utils import *

#======================
#    MISC FUNCTIONS
#======================
def scaleFactorCalc(exp, factor):
    return factor*10**exp


def xyToEN(x, y):
    """
    Converts (x, y) coordinates of prisms to (E, N) ones.
    It takes either single or array-like coordinates.
    """
    ref_x, ref_y = 15.184322095298622, -0.01676310147012092
    rot = np.deg2rad(37.1)
    e = x - ref_x
    n = y - ref_y
    eR = e*np.cos(rot) - n*np.sin(rot)
    nR = e*np.sin(rot) + n*np.cos(rot)

    return eR, nR


def interpolateRGB(start, end, n):
    """
    Returns *n* RGB color tuples interpolating
    linearly from start to end.
    Start and end must be list-like with rgb values.
    """
    fractions = np.linspace(0, 1, num=n)
    r = (end[0] - start[0])*fractions+start[0]
    g = (end[1] - start[1])*fractions+start[1]
    b = (end[2] - start[2])*fractions+start[2]
    colors = ['rgb({:0f},{:0f},{:0f})'.format(r[i], g[i], b[i]) for i in range(len(fractions))]
    return colors


def selectPrismSection(n):
    """
    NOTE: for now, the function excludes prisms in the
    1xx series.
    """
    full_section = {
        '01':['01','07'],
        '02':['02','08'],
        '03':['03','09'],
        '04':['04','10'],
        '05':['05','11'],
        '06':['06','12'],
        '07':['07','01'],
        '08':['08','02'],
        '09':['09','03'],
        '10':['10','04'],
        '11':['11','05'],
        '12':['12','06']
    }
    n = full_section[n]

    selected_sensors = [p for p in B_PRISM_POS.index if p.endswith(n[0]) and not (p.startswith('1'))]
    selected_sensors += [p for p in B_PRISM_POS.index if p.endswith(n[1]) and not (p.startswith('1'))]

    return selected_sensors


def rotTraslPrism(df, date):
    """
    Returns east and z coordinates of prisms
    in the DataFrame *df* for the date *date*.
    """
    x = df.loc[date, (slice(None), 'x')].values
    y = df.loc[date, (slice(None), 'y')].values
    z = df.loc[date, (slice(None), 'z')].values

    # Traslation
    ref_x, ref_y = 15.184322095298622, -0.01676310147012092
    x1 = x - ref_x
    y1 = y - ref_y

    # Rotation
    a = -np.arctan(y1/x1)
    east = x1*np.cos(a) - y1*np.sin(a)
    north = x1*np.sin(a) + y1*np.cos(a)

    if (north > 10**(-6)).any():
        print("ERROR: north coordinate is not zero")
        return 1

    return east, z



#==============================
#    TAB-SPECIFIC FUNCTIONS
#==============================

#----------------
#    INFO TAB
#----------------
def figureGantt(which):
    """
    Plots a Gantt chart with the temporal availability of data.
    Expects:
    - which = list of instrumentation to plot.
    Returns:
    - figure object
    """
    which_df = {'Prisms': B_PRISMS,
               'Levelling': B_LEVELLING,
               'Cracks': B_EXTENSIMETERS}

    fig = go.Figure(layout_template=None)

    for i, w in enumerate(which):
        df = which_df[w]
        my_index = df[~df.index.duplicated()].resample('D').ffill().index
        fig.add_trace(
            go.Scatter(x=my_index, y=[w]*len(my_index),
                   mode='markers', name=w,
                      marker_color=colors[i],
                      marker_size = 10,
                      marker_symbol='square')
        )

    fig = reformatPlot(fig, [750,400])
    fig.update_layout(dict(yaxis_range=(-0.5, len(which)-0.5)),
                     margin=dict(r=20, t=20))
    fig.update_layout(dict(showlegend=False))
    fig.update_layout(hovermode='x unified')
    fig.update_traces(hovertemplate="%{x}")
    return fig


#------------------
#    CHECKS TAB
#------------------
def figureLevellingChecks(levelling_data, prism_data, extensimeter_data):
    """
    Returns the contents of a div (a list), with plots of
    levelling data vs prism data (vertical component);
    each plot is contained in a separate Graph object.
    """
    levelling_pruned = levelling_data[[c for c in levelling_data.columns if c[0] == 'L']]
    corresponding_prisms = [str(p) for p in [205, 305, 206, 306, 207, 307, 208, 308, 209, 309, 210, 310, 211, 311, 212, 312, 201, 301, 202, 302, 203, 303, 204, 304]]
    prism_z_rel = ((x:= prism_data.loc[:, (corresponding_prisms, 'z')]) - x.iloc[0])*1000.

    def singleFigure(l,p,lname,pname):
        """
        Actually makes the plot. l and p must be array-like or Series
        with relative vertical displacements of levelling and prism,
        respectively.
        """
        fig = go.Figure(layout_template=None)
        fig.update_layout(margin = dict(t=40, b=40))
        fig = make_subplots(specs=[[{"secondary_y": True}]],
                            figure=fig)
        fig = reformatPlot(fig, size=[1200, 350], secondary=True)

        fig.add_trace(
            go.Scatter(
                x=levelling_data.index,
                y=l,
                mode='markers+lines',
                name=lname,
                marker_color='#999933',
                line_color='#999933'
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=prism_data.index,
                y=p[:,0],
                mode='markers+lines',
                name=pname,
                marker_color='#882255',
                line_color='#882255'
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=extensimeter_data.index,
                y=extensimeter_data['F4F8', 'temp'].rolling(24).mean(),
                line_dash='dot',
                line_color='gray',
                name='Temperature'
            ),
            secondary_y = True,
        )

        fig.add_annotation(
            xref="x domain",
            yref="y domain",
            x=0.02,
            y=0.95,
            text='<b>'+ lname + '-' + pname +'</b>',
            font_family='Roboto',
            font_color='black',
            font_size=14,
            borderpad=4,
            bordercolor='black',
            borderwidth=1.5,
            showarrow=False
        )

        fig.update_yaxes(title_text="Displacement [mm]", secondary_y=False)
        fig.update_yaxes(title_text="Temperature [°C]", secondary_y=True)

        return fig

    children = []
    for lname, pname in zip(levelling_pruned.columns, corresponding_prisms):
        graph = dcc.Graph(figure=singleFigure(levelling_pruned[lname].values, prism_z_rel[pname].values, lname, pname))
        children.append(graph)

    return children

b_divchildren_levelling_checks = figureLevellingChecks(B_LEVELLING, B_PRISMS, B_EXTENSIMETERS)


#----------------
#    PLAN TAB
#----------------
def figurePrismPlan(daterange, scalefactor, floor, prism_data, prism_pos):
    """
    Produces a plot showing the displacement of prisms
    in plan.
    Expects:
    - daterange: a list of two integers within len(prism_data.index)
    - scalefactor: a number
    - floor: a list of strings, either/or "First" and "Second"
    Returns:
    - the plot
    """
    fig = go.Figure(layout_template=None)
    fig = reformatPlot(fig, size=[800,700])

    # Select prisms
    if floor == []:
        return fig
    if 'First' in floor:
        selected_prisms = [i for i in prism_pos.index if (x:=i[0]) == '2' or x=='3']
        if 'Second' in floor:
            selected_prisms += [i for i in prism_pos.index if (x:=i[0]) == '4' or x=='5']
    else:
        selected_prisms = [i for i in prism_pos.index if (x:=i[0]) == '4' or x=='5']
    df = prism_data.loc[:, (selected_prisms, slice(None))]

    # Get prism coordinates
    start_date = df.index[daterange[0]]
    end_date = df.index[daterange[1]]
    x_0 = df.loc[start_date, (slice(None), 'x')].values
    y_0 = df.loc[start_date, (slice(None), 'y')].values
    x_1 = df.loc[end_date, (slice(None), 'x')].values
    y_1 = df.loc[end_date, (slice(None), 'y')].values

    # Rotate prisms so that x is in the East direction
    # and translate them so that the origin is in the center
    # of the Baptistery
    eR_0, nR_0 = xyToEN(x_0, y_0)
    eR_1, nR_1 = xyToEN(x_1, y_1)
    east_diff = (eR_1 - eR_0) * scalefactor
    north_diff = (nR_1 - nR_0) * scalefactor
    eR_1 = eR_0 + east_diff
    nR_1 = nR_0 + north_diff

    # Plot prisms
    fig.add_trace(
        go.Scatter(x=eR_0[:12], y=nR_0[:12],
                   mode='lines+markers', name=str(start_date)[:10],
                   marker_size = 10,
                   marker_color = blues[1],
                   hovertext = ["Prism n. {}".format(i) for i in selected_prisms],
                   hoverinfo = 'text'
        )
    )
    fig.add_trace(
        go.Scatter(x=eR_1[:12], y=nR_1[:12],
                   mode='lines+markers', name=str(end_date)[:10],
                   marker_size = 10,
                   marker_color = blues[-2],
                   hovertext = ["Prism n. {}".format(i) for i in selected_prisms],
                   hoverinfo = 'text'
        )
    )
    
    fig.add_trace(
        go.Scatter(x=eR_0[12:], y=nR_0[12:],
                   mode='lines+markers', name=str(start_date)[:10],
                   marker_size = 10,
                   marker_color = blues[1],
                   hovertext = ["Prism n. {}".format(i) for i in selected_prisms],
                   hoverinfo = 'text',
                   showlegend=False
        )
    )
    fig.add_trace(
        go.Scatter(x=eR_1[12:], y=nR_1[12:],
                   mode='lines+markers', name=str(end_date)[:10],
                   marker_size = 10,
                   marker_color = blues[-2],
                   hovertext = ["Prism n. {}".format(i) for i in selected_prisms],
                   hoverinfo = 'text',
                   showlegend=False
        )
    )
    
    p_lines=[[0,11],[12,-1]]
    for p in p_lines:
        lines_eR0=np.array([eR_0[p[0]],eR_0[p[1]]])
        lines_nR0=np.array([nR_0[p[0]],nR_0[p[1]]])
        lines_eR1=np.array([eR_1[p[0]],eR_1[p[1]]])
        lines_nR1=np.array([nR_1[p[0]],nR_1[p[1]]])
    
        fig.add_trace(
        go.Scatter(x=lines_eR0, y=lines_nR0,
                   mode='lines', name=str(end_date)[:10],
                   marker_size = 10,
                   marker_color = blues[1],
                   hovertext = ["Prism n. {}".format(i) for i in selected_prisms],
                   hoverinfo = 'text',
                   showlegend=False
        )
    )
    
        fig.add_trace(
        go.Scatter(x=lines_eR1, y=lines_nR1,
                   mode='lines', name=str(end_date)[:10],
                   marker_size = 10,
                   marker_color = blues[-2],
                   hovertext = ["Prism n. {}".format(i) for i in selected_prisms],
                   hoverinfo = 'text',
                   showlegend=False
        )
    )

    # Plot lines connecting corresponding points
    for i in range(len(eR_0)):
        fig.add_shape(type="line",
            x0=eR_0[i], y0=nR_0[i],
            x1=eR_1[i], y1=nR_1[i],
            line=dict(
                color="lightgrey",
                width=2,
                dash="dot"
            ))

    # Add the shape of the Baptistery
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-17.80, y0=-17.80, x1=17.80, y1=17.80,
        line_color="black",
        line_width=0.75,
    )

    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-15.25, y0=-15.25, x1=15.25, y1=15.25,
        line_color="black",
        line_width=0.75,
    )

    # Format plot
    fig.update_layout(dict(
        xaxis_range = (-25, 25),
        yaxis_range = (-25, 25),
    ),
        margin=dict(t=40)
                     )
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
      )

    return fig


#-------------------
#    SECTION TAB
#-------------------
def figureSectionSelection(selected_prisms, prism_pos):
    """
    A small figure showing which section was selected.
    """
    fig = go.Figure(layout_template='plotly_white')
    fig.update_layout(height=250, width=250,
                         margin=dict(l=0,r=0,b=0,t=0))

    unselected_prisms = [el for el in prism_pos.index if (el not in selected_prisms and el[0] != '1')]
    up_x = [(a:=prism_pos.loc[i])['radius'] * np.cos(np.deg2rad(a['angle']))
            for i in unselected_prisms]
    up_y = [(a:=prism_pos.loc[i])['radius'] * np.sin(np.deg2rad(a['angle']))
            for i in unselected_prisms]
    sp_x = [(a:=prism_pos.loc[i])['radius'] * np.cos(np.deg2rad(a['angle']))
            for i in selected_prisms]
    sp_y = [(a:=prism_pos.loc[i])['radius'] * np.sin(np.deg2rad(a['angle']))
            for i in selected_prisms]

    # Add the shape of the Baptistery
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-17.80, y0=-17.80, x1=17.80, y1=17.80,
        line_color="lightgrey"
    )
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-15.25, y0=-15.25, x1=15.25, y1=15.25,
        line_color="lightgrey",
        line_width=1
    )

    # Add unselected prisms
    fig.add_trace(
        go.Scatter(x=up_x, y=up_y,
                  mode='markers',
                  marker_color='lightblue',
                  hovertext=['Prism n. {}'.format(i)
                             for i in unselected_prisms],
                  hoverinfo='text'
                  )
    )

    # Add selected prisms
    fig.add_trace(
        go.Scatter(x=sp_x, y=sp_y,
                  mode='markers',
                  marker_color='red',
                  hovertext=['Prism n. {}'.format(i)
                             for i in selected_prisms],
                  hoverinfo='text'
                  )
    )

    # Disable the legend
    fig.update(layout_showlegend=False)
    # Format plot
    fig.update_layout(dict(
        xaxis_range = (-20, 20),
        yaxis_range = (-20, 20),
        xaxis_zeroline = False,
        xaxis_showgrid = False,
        yaxis_zeroline = False,
        yaxis_showgrid = False,
        xaxis_visible = False,
        yaxis_visible = False
    ))
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
      )

    return fig


def figurePrismSection(selected_prisms, daterange, scalefactor, fixedbase, prism_data):
    """
    Produces a plot showing the displacement of prisms in a given section.
    Expects:
    - selected_prisms: a list of prism names
    - daterange: a list of two integers within len(prism_data.index)
    - scalefactor: a number
    - fixedbase: boolean
    Returns:
    - the plot
    """

    # This part assumes that the prisms in each
    # section use the same naming convention
    selected_prisms.sort()
    links = [
        [0, 4],
        [1, 5],
        [2, 6],
        [3, 7]
    ]

    fig = go.Figure(layout_template = None)
    fig = reformatPlot(fig, size=[800, 700])
    fig.update_layout(
        margin=dict(t=40)
    )

    # Prune dataframe
    df = prism_data.loc[:, (selected_prisms, slice(None))]
    # Selection dates
    numdate = daterange[1] - daterange[0] + 1
    dates = [df.index[daterange[0]], df.index[daterange[1]]]
    # Colors
    colors = ['rgb(255, 198, 196)', 'rgb(103, 32, 68)']

    e0, z0 = rotTraslPrism(df, dates[0])
    fig.add_trace(
        go.Scatter(
            x=e0, y=z0,
            name=(ddd:=str(dates[0])[:10]),
            mode='markers', marker_size=10,
            marker_color=colors[0],
            hovertext=['Prism n. {}\n{}'.format(i, ddd)
                          for i in selected_prisms],
                hoverinfo='text'
        )
    )
    for l in links:
        fig.add_shape(type="line",
            x0=e0[l[0]], y0=z0[l[0]],
            x1=e0[l[1]], y1=z0[l[1]],
            line=dict(
                color=colors[0],
                width=2,
            ))

        if fixedbase:
            fig.add_shape(type='line',
                     x0=e0[l[0]], y0=z0[l[0]],
                     x1=e0[l[0]], y1=0.0,
                     line=dict(
                         color=colors[0],
                         width=1,
                         dash='dash'
                     ))

    for i, d in enumerate(dates[1:]):
        e, z  = rotTraslPrism(df, d)
        diff_e = e-e0
        diff_z = z-z0
        e = e0 + diff_e * scalefactor
        z = z0 + diff_z * scalefactor
        fig.add_trace(
            go.Scatter(
                x = e, y = z,
                mode = 'markers', marker_size=10,
                name = (ddd:=str(d)[:10]),
                marker_color=colors[i+1],
                hovertext=['Prism n. {}\n{}'.format(i,ddd)
                          for i in selected_prisms],
                hoverinfo='text'
            )
        )
        for l in links:
            fig.add_shape(type="line",
                x0=e[l[0]], y0=z[l[0]],
                x1=e[l[1]], y1=z[l[1]],
                line=dict(
                    color=colors[i+1],
                    width=1
                ))

            if fixedbase:
                fig.add_shape(type='line',
                             x0=e[l[0]], y0=z[l[0]],
                             x1=e0[l[0]], y1=0.0,
                             line=dict(
                                 color=colors[i+1],
                                 width=1,
                                 dash='dash'
                             ))
    return fig


def figureSectionRelativeDisplacements(prisms, prism_data, extensimeter_data):
    """
    Produces a plot with the relative displacements of
    corresponding prisms in a section.
    """
    fig = go.Figure(layout_template=None)
    fig.update_layout(margin = dict(t=40, b=40))
    fig = make_subplots(specs=[[{"secondary_y": True}]],
                        figure=fig)
    fig = reformatPlot(fig, size=[900, 350], secondary=True)

    dists = np.sqrt(((prism_data[prisms[1]] - prism_data[prisms[0]])**2).sum(axis=1))*1000
    rel_disp = dists - dists[0]

    fig.add_trace(
        go.Scatter(
            x=prism_data.index,
            y=rel_disp,
            mode='markers+lines',
            name='Relative displacement',
            marker_color='#009988',
            line_color='#009988'
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=extensimeter_data.index,
            y=extensimeter_data['F4F8', 'temp'].rolling(24).mean(),
            line_dash='dot',
            line_color='gray',
            name='Temperature'
        ),
        secondary_y = True,
    )

    fig.add_annotation(
        xref="x domain",
        yref="y domain",
        x=0.02,
        y=0.95,
        text='<b>'+prisms[0] + '-' + prisms[1]+'</b>',
        font_family='Roboto',
        font_color='black',
        font_size=14,
        borderpad=4,
        bordercolor='black',
        borderwidth=1.5,
        showarrow=False
    )

    fig.update_yaxes(title_text="Displacement [mm]", secondary_y=False)
    fig.update_yaxes(title_text="Temperature [°C]", secondary_y=True)

    fig.update_layout(
        legend=dict(
            x=0.70, y=0.95
        )
    )

    return fig


def figurePrismCoupleSelection(selected_prisms, prism_pos):
    """
    A small figure showing which couple of prisms was selected.
    """
    fig = go.Figure(layout_template='plotly_white')
    fig.update_layout(height=250, width=250,
                         margin=dict(l=0,r=0,b=0,t=0))

    unselected_prisms = [el for el in prism_pos.index if (el not in selected_prisms and el[0] != '1')]
    up_x = [(a:=prism_pos.loc[i])['radius'] * np.cos(np.deg2rad(a['angle']))
            for i in unselected_prisms]
    up_y = [(a:=prism_pos.loc[i])['radius'] * np.sin(np.deg2rad(a['angle']))
            for i in unselected_prisms]
    sp_x = [(a:=prism_pos.loc[i])['radius'] * np.cos(np.deg2rad(a['angle']))
            for i in selected_prisms]
    sp_y = [(a:=prism_pos.loc[i])['radius'] * np.sin(np.deg2rad(a['angle']))
            for i in selected_prisms]

    # Add the shape of the Baptistery
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-17.80, y0=-17.80, x1=17.80, y1=17.80,
        line_color="lightgrey"
    )
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-15.25, y0=-15.25, x1=15.25, y1=15.25,
        line_color="lightgrey",
        line_width=1
    )

    # Add unselected prisms
    fig.add_trace(
        go.Scatter(x=up_x, y=up_y,
                  mode='markers',
                  marker_color='lightblue',
                  hovertext=['Prism n. {}'.format(i)
                             for i in unselected_prisms],
                  hoverinfo='text'
                  )
    )

    # Add selected prisms
    fig.add_trace(
        go.Scatter(x=sp_x, y=sp_y,
                  mode='markers+text',
                  text=selected_prisms,
                  textfont_family='Roboto',
                  textposition='top center',
                  textfont_size=12,
                  marker_color='red',
                  hovertext=['Prism n. {}'.format(i)
                             for i in selected_prisms],
                  hoverinfo='text'
                  )
    )

    # Connecting line
    fig.add_shape(type="line",
            x0=sp_x[0], y0=sp_y[0],
            x1=sp_x[1], y1=sp_y[1],
            line=dict(
                color='gray',
                width=2,
                dash='dash'
            ))

    # Disable the legend
    fig.update(layout_showlegend=False)
    # Format plot
    fig.update_layout(dict(
        xaxis_range = (-20, 20),
        yaxis_range = (-20, 20),
        xaxis_zeroline = False,
        xaxis_showgrid = False,
        yaxis_zeroline = False,
        yaxis_showgrid = False,
        xaxis_visible = False,
        yaxis_visible = False
    ))
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
      )

    return fig


#------------------
#    PRISMS TAB
#------------------
def figurePrismSelection(prism_pos):
    """
    A figure from which to select prisms.
    """
    fig = go.Figure(layout_template='plotly_white')

    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=('Ground floor', 'First floor', 'Second floor'),
                        figure=fig
                       )
    fig.update_layout(height=350, width=1000,
                         margin=dict(l=0,r=0,b=0,t=60))

    ground_floor = ['101', '102', '103', '104', 'P1']
    first_floor = [p for p in prism_pos.index if (p[0] == '2' or p[0] == '3')]
    second_floor = [p for p in prism_pos.index if (p[0] == '4' or p[0] == '5')]

    floors = [ground_floor, first_floor, second_floor]

    for i, f in enumerate(floors):
        x = prism_pos.loc[f]['radius']*np.cos(np.deg2rad(prism_pos.loc[f]['angle']))
        y = prism_pos.loc[f]['radius']*np.sin(np.deg2rad(prism_pos.loc[f]['angle']))
        # Add the shape of the Baptistery
        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=-17.80, y0=-17.80, x1=17.80, y1=17.80,
            line_color="lightgrey",
            row=1, col=i+1
        )
        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=-15.25, y0=-15.25, x1=15.25, y1=15.25,
            line_color="lightgrey",
            line_width=1,
            row=1, col=i+1
        )
        # Add the prisms
        fig.add_trace(
            go.Scatter(
                x=x, y=y,
                customdata=f,
                text=f,
                textfont_size=10,
                textposition='top center',
                mode='markers+text',
                marker_color=colors[1],
                hovertext=['Prism n. {}'.format(p)
                             for p in f],
                marker_size=10,
                hoverinfo='text',
                selected_marker_color='red'
              ),
            row=1, col=i+1
        )

    # Disable the legend
    fig.update(layout_showlegend=False)

    # Format plot
    fig.update_xaxes(
        range = (-18, 18),
        zeroline = False,
        showgrid = False,
        visible = False,
    )
    fig.update_yaxes(
        range = (-18, 18),
        zeroline = False,
        showgrid = False,
        visible = False,
    )
    fig.update_layout(
        yaxis1=dict(
        scaleanchor = "x1",
        scaleratio = 1,
        )
    )
    fig.update_layout(
        yaxis2=dict(
        scaleanchor = "x2",
        scaleratio = 1,
        )
    )
    fig.update_layout(
        yaxis3=dict(
        scaleanchor = "x3",
        scaleratio = 1,
        )
    )

    fig.update_layout(clickmode='event+select')

    return fig

b_fig_prism_selection = figurePrismSelection(B_PRISM_POS)


def figurePrismDisplacementTogether(p_list, component, prism_data, extensimeter_data):
    """
    Produces a figure with the displacement of the prisms contained in
    *p_list*. You can choose which component to plot.
    """

    fig = go.Figure(layout_template=None)
    fig.update_layout(
        margin = dict(t=40, b=40),
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]],
                        shared_xaxes=True,
                        vertical_spacing=0.0,
                        figure=fig)
    fig = reformatPlot(fig, size=[1200, 350], secondary=True)

    for p in p_list:
        x = prism_data[p, 'x'].values
        y = prism_data[p, 'y'].values
        z = prism_data[p, 'z'].values*1000.
        e, n = xyToEN(x, y)
        e = e*1000.
        n = n*1000.

        de = e - np.array(e).mean()
        dn = n - np.array(n).mean()
        dz = z - np.array(z).mean()


        dtot = np.sqrt(de**2 + dn**2 + dz**2)

        r = np.sqrt(e**2 + n**2)
        dr = r - np.array(r).mean()


        alpha = np.arctan(n/e)
        dalpha = alpha - alpha[0]
        dtan = r*np.sin(dalpha)

        # Dictionary with components and colors [now unused]
        components_dict = {
            'Total': [dtot, colors4[0]],
            'Radial': [dr, colors4[1]],
            'Tangential': [dtan, colors4[2]],
            'Vertical': [dz, colors4[3]]
        }


        fig.add_trace(
            go.Scatter(
                x=prism_data.index,
                y=components_dict[component][0],
                mode='markers+lines',
                name=p,
            ),
            secondary_y = False,
        )

    # Temperature
    fig.add_trace(
        go.Scatter(
            x=extensimeter_data.index,
            y=extensimeter_data['F4F8', 'temp'].rolling(24).mean(),
            line_dash='dot',
            line_color='gray',
            name='Temperature'
        ),
        secondary_y = True,
    )

    fig.add_annotation(
        xref="x domain",
        yref="y domain",
        x=0.02,
        y=0.95,
        text='<b>'+component+'</b>',
        font_family='Roboto',
        font_color='black',
        font_size=14,
        borderpad=4,
        bordercolor='black',
        borderwidth=1.5,
        showarrow=False
    )

    fig.update_yaxes(title_text="Displacement [mm]", secondary_y=False)
    fig.update_yaxes(title_text="Temperature [°C]", secondary_y=True)

    return fig


def figurePrismDisplacement(p, prism_data, extensimeter_data):
    """
    Produces a figure with the displacement of the *p*
    prism. Both the total one and single components.
    """

    fig = go.Figure(layout_template=None)
    fig.update_layout(
        margin = dict(t=40, b=40),
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]],
                        shared_xaxes=True,
                        vertical_spacing=0.0,
                        figure=fig)
    fig = reformatPlot(fig, size=[1200, 350], secondary=True)

    x = prism_data[p, 'x'].values
    y = prism_data[p, 'y'].values
    z = prism_data[p, 'z'].values*1000.
    e, n = xyToEN(x, y)
    e = e*1000.
    n = n*1000.

    de = e - e[0]
    dn = n - n[0]
    dz = z - z[0]

    dtot = np.sqrt(de**2 + dn**2 + dz**2)

    r = np.sqrt(e**2 + n**2)
    dr = r - r[0]

    alpha = np.arctan(n/e)
    dalpha = alpha - alpha[0]
    dtan = r*np.sin(dalpha)

    traces = [dtot, dr, dtan, dz]
    names = ['Total', 'Radial', 'Tangential', 'Vertical']

    for t,n,c in zip(traces, names, colors4):
        fig.add_trace(
            go.Scatter(
                x=prism_data.index,
                y=t,
                mode='markers+lines',
                name=n,
                marker_color = c,
                line_color = c,
            ),
            secondary_y = False,
        )

    fig.add_trace(
        go.Scatter(
            x=extensimeter_data.index,
            y=extensimeter_data['F4F8', 'temp'].rolling(24).mean(),
            line_dash='dot',
            line_color='gray',
            name='Temperature'
        ),
        secondary_y = True,
    )

    fig.add_annotation(
        xref="x domain",
        yref="y domain",
        x=0.02,
        y=0.95,
        text='<b>'+p+'</b>',
        font_family='Roboto',
        font_color='black',
        font_size=14,
        borderpad=4,
        bordercolor='black',
        borderwidth=1.5,
        showarrow=False
    )

    fig.update_yaxes(title_text="Displacement [mm]", secondary_y=False)
    fig.update_yaxes(title_text="Temperature [°C]", secondary_y=True)

    return fig


#------------------
#    CRACKS TAB
#------------------
def figureExtensimeter(e, extensimeter_data, resampling='W'):
    """
    Plots extensimeter data with the corresponding temperature.
    """
    crack = extensimeter_data.loc[:, (e, 'pos')].resample(resampling).mean()
    temp = extensimeter_data.loc[:, (e, 'temp')].resample(resampling).mean()
    index = extensimeter_data.resample(resampling).mean().index

    fig = go.Figure(layout_template=None)
    fig.update_layout(margin = dict(t=40, b=40))
    fig = make_subplots(specs=[[{"secondary_y": True}]],
                        figure=fig)
    fig = reformatPlot(fig, size=[950, 350], secondary=True)

    if (resampling == 'W' or resampling == 'M'):
        mode = 'markers+lines'
    else:
        mode = 'lines'

    fig.add_trace(
        go.Scatter(
            x=index,
            y=crack,
            mode=mode,
            name='Crack width',
            marker_color='#DDCC77',
            line_color='#DDCC77'
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=index,
            y=temp,
            line_dash='dot',
            line_color='gray',
            name='Temperature'
        ),
        secondary_y = True,
    )

    fig.add_annotation(
        xref="x domain",
        yref="y domain",
        x=0.02,
        y=0.95,
        text='<b>'+ e +'</b>',
        font_family='Roboto',
        font_color='black',
        font_size=14,
        borderpad=4,
        bordercolor='black',
        borderwidth=1.5,
        showarrow=False
    )

    fig.update_yaxes(title_text="Crack width [mm]", secondary_y=False)
    fig.update_yaxes(title_text="Temperature [°C]", secondary_y=True)

    fig.update_layout(
        legend=dict(
            x=0.78, y=0.05
        )
    )

    return fig


def figureExtensimeterSelection(e, extensimeter_pos):
    """
    Small plot indicating the position of
    extensimeter *e*.
    """
    fig = go.Figure(layout_template='plotly_white')
    fig.update_layout(height=250, width=250,
                         margin=dict(l=0,r=0,b=0,t=0))

    unselected_ext = [e for e in extensimeter_pos.index]
    unselected_ext.remove(e)
    unselected_ext.remove('F4F8') #Removes the thermometer
    ue_x = [(a:=extensimeter_pos.loc[i])['radius'] * np.cos(np.deg2rad(a['angle']))
            for i in unselected_ext]
    ue_y = [(a:=extensimeter_pos.loc[i])['radius'] * np.sin(np.deg2rad(a['angle']))
            for i in unselected_ext]
    se_x = [(a:=extensimeter_pos.loc[e])['radius'] * np.cos(np.deg2rad(a['angle']))]
    se_y = [(a:=extensimeter_pos.loc[e])['radius'] * np.sin(np.deg2rad(a['angle']))]

    # Add the shape of the Baptistery
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-17.80, y0=-17.80, x1=17.80, y1=17.80,
        line_color="lightgrey"
    )
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-15.25, y0=-15.25, x1=15.25, y1=15.25,
        line_color="lightgrey",
        line_width=1
    )

    # Add unselected extensimeters
    fig.add_trace(
        go.Scatter(x=ue_x, y=ue_y,
                  mode='markers',
                  marker_color='lightblue',
                  hovertext=['Extensimeter {}'.format(i)
                             for i in unselected_ext],
                  hoverinfo='text'
                  )
    )

    # Add selected extensimeters
    fig.add_trace(
        go.Scatter(x=se_x, y=se_y,
                  mode='markers+text',
                  text=[e],
                  textfont_family='Roboto',
                  textposition='top center',
                  textfont_size=12,
                  marker_color='red',
                  hovertext=['Extensimeter {}'.format(e)],
                  hoverinfo='text'
                  )
    )


    # Disable the legend
    fig.update(layout_showlegend=False)
    # Format plot
    fig.update_layout(dict(
        xaxis_range = (-20, 20),
        yaxis_range = (-20, 20),
        xaxis_zeroline = False,
        xaxis_showgrid = False,
        yaxis_zeroline = False,
        yaxis_showgrid = False,
        xaxis_visible = False,
        yaxis_visible = False
    ))
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
      )

    return fig


b_extensimeter_positions = [figureExtensimeterSelection(e, B_EXTENSIMETER_POS) for e in ['F3CE', 'F3CF', 'F3D1', 'F3D2', 'F46C', 'F46D', 'F3D0', 'F46B']]

#------------------
#    3D TAB
#------------------

def figurePrism3d(prism_data,daterange, scalefactor, zero_floor, conn_matrix):
    """
    Produces a plot showing the displacement of prisms
    in 3d.
    Expects:
    - daterange: a list of two integers within len(prism_data.index)
    - scalefactor: a number
    - zero_floor: a boolean, if True includes the zero_floor in the graph. 
    Returns:
    - the plot
    """
    if zero_floor:
        prism_data_3d=prism_data.copy()
    else:
        prism_data_3d=prism_data.copy().iloc[:,12:]
        conn_matrix=conn_matrix.iloc[[1,2,3,4]+list(range(9,33,1))]
        
    prism_name=np.unique([prism_data_3d.columns[el][0] for el in range(prism_data_3d.shape[1])])
    dates=[prism_data_3d.index[daterange[0]],prism_data_3d.index[daterange[1]]]
    prism_start=prism_data_3d.loc[dates[0]:]
    prism_disp=pd.DataFrame((prism_start-prism_start.iloc[0]).values*scalefactor+prism_start.iloc[0,:].values)
    prism_disp.index=prism_start.index
    prism_disp.columns=prism_start.columns
    
    data = {
        'start': [prism_data_3d.loc[dates[0]], 0.4,],
        'end': [prism_disp.loc[dates[1]], 1]
        
    }
    data_keys=['start','end']
    tot=pd.concat([prism_data_3d.loc[dates[0]],prism_disp.loc[dates[1]]],axis=1)
    tot=tot.T
    
    fig = go.Figure()
    
    for k in data_keys:
        for n in range(1,6):
            prism_elements=[]
            for el in prism_name:
                 if el.startswith(str(n)):
                    prism_elements.append(el)
            fig.add_trace(go.Scatter3d(
                    x=data[k][0].loc[ (prism_elements, 'x')],
                       y=data[k][0].loc[ (prism_elements, 'y')], 
                       z=data[k][0].loc[(prism_elements, 'z')],
                mode='markers+lines',
                marker_size=5,
                marker_color= '#3182bd',
                showlegend=False,
                opacity=data[k][1],
                text=prism_elements,
                hoverinfo='text'
                                ))
    
        for row in range(len(conn_matrix.index)):
            fig.add_trace(go.Scatter3d(
            x=data[k][0].loc[ (list(conn_matrix.iloc[row,:].values), 'x')],
            y=data[k][0].loc[ (list(conn_matrix.iloc[row,:].values), 'y')] ,
            z=data[k][0].loc[ (list(conn_matrix.iloc[row,:].values), 'z')],
            mode='lines',
            line_color='#3182bd',
            showlegend=False,
            opacity=data[k][1],
            line_width=2,
            line_dash=None,
            hoverinfo=None,
        
        ))
            
    for p in prism_name[:-1]:
        fig.add_trace(go.Scatter3d(
        x=tot.loc[:,(p, 'x')],
        y=tot.loc[:,(p, 'y')],
        z=tot.loc[:,(p, 'z')],
        mode='lines',
        line_dash='dash',
        line_color='grey',
        line_width=5,
        showlegend=False,
        hoverinfo=None
    ))
    
    fig.update_layout(scene=dict(
        xaxis=dict(range=[-10, 40]),
        yaxis=dict(range=[-25, 25]),
        zaxis=dict(range=[0, 35]),
    ),height=900, width=900,margin=dict(l=0, r=0, b=0, t=0)
    
    )
    
              
    return fig
