import plotly.graph_objects as go
import plotly.io as pio
import plotly.utils as pu
from metno_locationforecast import Place, Forecast
from .met import metno_temperatur, metno_nedbør
from .stasjon import hent_frost, vindrose
import json
from datetime import datetime, timedelta
from dateutil.parser import parse
import numpy as np
import pandas as pd

def vaerplot(lat, lon, navn, altitude, stasjonsid, elements):
    dager_tidligere = 4
    user_agent = "Stedspesifikk v/0.1 jan.helge.aalbu@vegvesen.no"
    vaer = Place(navn, lat, lon, altitude)
    vaer_forecast = Forecast(vaer, user_agent)
    vaer_forecast.update()
    time_nebør, nedbør = metno_nedbør(vaer_forecast, dager_tidligere)

    time_temperatur, temperatur = metno_temperatur(vaer_forecast, dager_tidligere)

    nedbør_cumsum = np.cumsum(nedbør).tolist()

    line_elements = ['air_temperature', 'wind_speed']
    bar_elements = ['sum(precipitation_amount PT10M)']


    # Lager til figuren
    fig = go.Figure()

    #Plotter ut data fra yr apiet
    fig.add_trace(go.Bar(x=time_nebør, y=nedbør, name='Nedbør (YR)', width=1000 * 3600 * 5, yaxis='y2'))
    fig.add_trace(go.Scatter(x=time_temperatur, y=temperatur, mode='lines', name='temperatur (YR)'))
    fig.add_trace(go.Scatter(x=time_nebør, y=nedbør_cumsum, mode='lines', name='Kumulativ nedbør (YR)', fill='tozeroy', fillcolor='rgba(0, 0, 255, 0.1)', yaxis='y3'))
    
    #Henter ut data fra forst apiet
    værhist = hent_frost(stasjonsid, dager_tidligere, elements, timeoffsets='PT0H')

    for element in værhist:
        if element == 'sum(precipitation_amount PT10M)':
            fig.add_trace(go.Bar(x=værhist[element]['referenceTime'], y=værhist[element]['value'], name='Nedbør (YR)', width=1000 * 3600 * 1, yaxis='y2'))
        else:
            fig.add_trace(go.Scatter(x=værhist[element]['referenceTime'], y=værhist[element]['value'], mode='lines', name=element))
    #fig.add_trace(go.Bar(x=time_nebør, y=nedbør, name='nedbør', width=1000 * 3600 * 5))
    #fig.add_trace(go.Scatter(x=df['referenceTime'], y=df['value'], mode='lines', name='Temperatur (værstasjon)'))

    fig.update_layout(
        yaxis=dict(
            title='Temperatur',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            )
        ),
        yaxis2=dict(
            title='Nedbør',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        ),
        yaxis3=dict(
            title='Kumulativ nedbør',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        ),
    )
    fig_json = json.loads(fig.to_json())
    # Convert the graph to JSON format
    return json.dumps(fig_json, safe=False)

def met_plot(lat, lon, navn, altitude, dager=4):
    user_agent = "Stedspesifikk v/0.1 jan.helge.aalbu@vegvesen.no"
    vaer = Place(navn, lat, lon, altitude)
    vaer_forecast = Forecast(vaer, user_agent)
    vaer_forecast.update()
    time_nebør, nedbør = metno_nedbør(vaer_forecast, dager)

    time_temperatur, temperatur = metno_temperatur(vaer_forecast, dager)

    nedbør_cumsum = np.cumsum(nedbør).tolist()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=time_nebør, y=nedbør, name='Nedbør (YR)', width=1000 * 3600 * 5, yaxis='y2'))
    fig.add_trace(go.Scatter(x=time_temperatur, y=temperatur, mode='lines', name='temperatur (YR)'))
    fig.add_trace(go.Scatter(x=time_nebør, y=nedbør_cumsum, mode='lines', name='Kumulativ nedbør (YR)', fill='tozeroy', fillcolor='rgba(0, 0, 255, 0.1)', yaxis='y3'))
    fig.update_layout(
        yaxis=dict(
            title='Temperatur',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            )
        ),
        yaxis2=dict(
            title='Nedbør',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        ),
        yaxis3=dict(
            title='Kumulativ nedbør',
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        ),
    )
    
    return fig
    # trace_nedbør_cumsum = {
    #     'x': time_nebør,
    #     'y': nedbør_cumsum,
    #     'type': 'scatter',
    #     'name': 'Kumulativ nedbør',
    #     'fill': 'tozeroy',
    #     'fillcolor': 'rgba(0, 0, 255, 0.1)', 
    #     'yaxis': 'y3',
    # }

    # trace_nedbør = {
    #     'x': time_nebør,
    #     'y': nedbør,
    #     'type': 'bar',
    #     'name': 'Nedbør',
    #     'width': 500 * 3600 * (dager/2),
    #     'yaxis': 'y2',
 
    # }
    # trace_temperatur = {
    #     'x': time_temperatur,
    #     'y': temperatur,
    #     'type': 'scatter',
    #     'name': 'Temperatur',
    #     'marker': {'color': 'red'},
    # }
    # traces = [trace_nedbør_cumsum, trace_nedbør, trace_temperatur]

    # layout = {
    #     'yaxis2': {
    #         'title': 'Nedbør',
    #         'overlaying': 'y',
    #         'side': 'right',
    #         'showgrid': False,  # Hide the grid lines
    #         'range': [min(nedbør_cumsum), max(nedbør_cumsum)]  # Set the same range as yaxis3
    #     },
    #     'yaxis': {
    #         'title': 'Temperatur',
    #         'showgrid': False,  # Hide the grid lines
    #     },
    #     'yaxis3': {  # Add a second y-axis
    #         'title': 'Nedbør',
    #         'overlaying': 'y',
    #         'side': 'right',
    #         'showgrid': False,  # Hide the grid lines
    #         'zeroline': False,  # Hide the zero line
    #         'range': [min(nedbør_cumsum), max(nedbør_cumsum)]  # Set the range based on your data
    #     },
    # }


    #return {'data': traces, 'layout': layout}

def frostplot_temp_nedbør_snø(stasjonsid, dager, elements):
    traces = []
    max_snødybde = 0
    for element in elements:
        print(element)
        #print(traces)
        if element == 'sum(precipitation_amount PT10M)':
            print('Inne i nedbør')
            tid, verdi = hent_frost(stasjonsid, dager, element, timeoffsets='PT0H')
            trace = {
            'x': tid,
            'y': verdi,
            'type': 'bar',
            'name': 'Nedbør',
            'marker': {'color': 'blue'},
            'width': 1000 * 3600 * 5,
            'yaxis': 'y2'
            }
            traces.append(trace)
        elif element == 'air_temperature':
            print('Inne i temperatur')
            tid, verdi = hent_frost(stasjonsid, dager, element, timeoffsets='PT0H')
            trace = {
            'x': tid,
            'y': verdi,
            'type': 'scatter',
            'name': 'Temperatur',
            'marker': {'color': 'red'},
            'yaxis': 'y'
            }
            traces.append(trace)
        elif element == 'surface_snow_thickness':
            print('Inne i snødybde')
            tid, verdi = hent_frost(stasjonsid, dager, element, timeoffsets='PT0H')
            trace = {
            'x': tid,
            'y': verdi,
            'type': 'scatter',
            'name': 'Snødybde',
            'marker': {'color': 'blue'},
            'fill': 'tozeroy',
            'fillcolor': 'rgba(0, 0, 255, 0.1)', 
            'yaxis': 'y3'
            }
            traces.append(trace)

            max_snødybde = max((v for v in verdi if v is not None), default=None)
    layout = {
        'yaxis2': {
            'title': 'Nedbør',
            'overlaying': 'y',
            'side': 'right',
            'showgrid': False,
            'position': 0.85,  # Hide the grid lines
        },
        'yaxis': {
            'title': 'Temperatur',
            'showgrid': False,  # Hide the grid lines
        },
        'yaxis3': {  # Add a second y-axis
            'title': 'Snødybde',
            'overlaying': 'y',
            'side': 'right',
            'showgrid': False,  # Hide the grid lines
            'zeroline': False,  # Hide the zero line
            'position': 0.90,
            'range': [0.3*max_snødybde, max_snødybde+0.3*max_snødybde] 
        },
        'xaxis': {'domain': [0.0, 0.8]},
    }
    return {'data' : traces, 'layout': layout}

def frostplot_vind(stasjonsid, dager, elements):
    traces = []

    for element in elements:
        print(element)
        #print(traces)
        if element == 'wind_from_direction':
            print('Inne i wind_from_direction')
            tid, verdi = hent_frost(stasjonsid, dager, element, timeoffsets='PT0H')
            trace = {
            'x': tid,
            'y': verdi,
            'type': 'scatter',
            'name': 'Vindretning',
            'marker': {'color': 'blue'},
            'yaxis': 'y'
            }
            traces.append(trace)
        elif element == 'wind_speed':
            print('Inne i wind_speed')
            tid, verdi = hent_frost(stasjonsid, dager, element, timeoffsets='PT0H')
            trace = {
            'x': tid,
            'y': verdi,
            'type': 'scatter',
            'name': 'Vindhastighet',
            'marker': {'color': 'red'},
            'yaxis': 'y2'
            }
            traces.append(trace)

    layout = {
        'yaxis': {
            'title': 'Vindretning',
            'showgrid': False,

        },
        'yaxis2': {
            'title': 'Vindestyrke',
            'side': 'right',
            'showgrid': False,  # Hide the grid lines
            'overlaying': 'y'
        },

    }
    return {'data' : traces, 'layout': layout}
    # return {'data' : traces}



def frost_windrose(stasjonsid, dager):
    retning_tekst = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    retning_grader = [0, 22.5, 45, 72.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
    vind_hastighet = ['0-4 m/s', '6-8 m/s', '9-11 m/s', '11-14 m/s', '15-17 m/s', '17-20 m/s', '20-25 m/s', '>25 m/s']

    tid, retning = hent_frost(stasjonsid, dager, 'wind_speed', timeoffsets='PT0H')
    tid, hastighet = hent_frost(stasjonsid, dager, 'wind_from_direction', timeoffsets='PT0H')

    trace = {
        'type': 'barpolar',
        'r': retning,
        'theta': hastighet,
        'name': 'Vind',
        'marker': {'color': 'blue'},
    }

    layout = {
        'title': 'Wind Rose Plot',
        'font': {
            'size': 16
        },
        'radialaxis': {
            'ticksuffix': '%'
        },
        'orientation' : 270
    }

    return {'data': [trace], 'layout': layout}



def windrose_test():
    fig = go.Figure()

    fig.add_trace(go.Barpolar(
        r=[77.5, 72.5, 70.0, 45.0, 22.5, 42.5, 40.0, 62.5],
        name='11-14 m/s',
        marker_color='rgb(106,81,163)'
    ))
    fig.add_trace(go.Barpolar(
        r=[57.5, 50.0, 45.0, 35.0, 20.0, 22.5, 37.5, 55.0],
        name='8-11 m/s',
        marker_color='rgb(158,154,200)'
    ))
    fig.add_trace(go.Barpolar(
        r=[40.0, 30.0, 30.0, 35.0, 7.5, 7.5, 32.5, 40.0],
        name='5-8 m/s',
        marker_color='rgb(203,201,226)'
    ))
    fig.add_trace(go.Barpolar(
        r=[20.0, 7.5, 15.0, 22.5, 2.5, 2.5, 12.5, 22.5],
        name='< 5 m/s',
        marker_color='rgb(242,240,247)'
    ))

    fig.update_traces(text=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'])
    fig.update_layout(
        title='Wind Speed Distribution in Laurel, NE',
        font_size=16,
        legend_font_size=16,
        polar_radialaxis_ticksuffix='%',
        polar_angularaxis_rotation=90,

    )
    fig_json = json.loads(fig.to_json())

    return fig_json


# def windrose_test(request):
#     traces = []
#     vind1 = {
#         'type': 'barpolar',
#         'r' : [77.5, 72.5, 70.0, 45.0, 22.5, 42.5, 40.0, 62.5],
#         'name': '11-14 m/s',
#         'marker' : {'color' : 'rgb(106,81,163)'}
#         }
#     vind2 = {
#         'type': 'barpolar',
#         'r' : [57.5, 50.0, 45.0, 35.0, 20.0, 22.5, 37.5, 55.0],
#         'name': '8-11 m/s',
#         'marker' : {'color' : 'rgb(158,154,200)'}
#         }
#     vind3 = {
#         'type': 'barpolar',
#         'r' : [40.0, 30.0, 30.0, 35.0, 7.5, 7.5, 32.5, 40.0],
#         'name': '5-8 m/s',
#         'marker' : {'color' : 'rgb(203,201,226)'}
#         }
#     vind4 = {
#         'type': 'barpolar',
#         'r' : [20.0, 7.5, 15.0, 22.5, 2.5, 2.5, 12.5, 22.5],
#         'name': '< 5 m/s',
#         'marker' : {'color' : 'rgb(242,240,247)'}
#         }
#     traces.append(vind4)
#     traces.append(vind3)
#     traces.append(vind2)
#     traces.append(vind1)

#     layout = {
#         'title': 'Vindrose',
#         'font': {
#             'size': 16
#         },
#         'polar': {
#             'radialaxis': {
#                 'ticksuffix': '%',
#             },
#             'angularaxis': {
#                 'direction' : 'clockwise',
#                 'rotation' : 90
#             }
#         }
#     }
#     # fig.update_traces(text=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'])
#     # fig.update_layout(
#     #     title='Wind Speed Distribution in Laurel, NE',
#     #     font_size=16,
#     #     legend_font_size=16,
#     #     polar_radialaxis_ticksuffix='%',
#     #     polar_angularaxis_direction='clockwise',
#     #     polar_angularaxis_rotation=90,

#     # )
#     # fig.show()
#     return {'data': traces, 'layout': layout}

def windrose_test2(stasjonsid, dager_tidligere):
    #TODO: Må finne ut av dette med plotly.to_json greiene. Går det greit å sende til frontent?
    df = vindrose(stasjonsid, dager_tidligere)
    vind_hastighet = ['0-4 m/s', '6-8 m/s', '9-11 m/s', '11-14 m/s', '15-17 m/s', '17-20 m/s', '20-25 m/s', '>25 m/s']
    # Assuming df is your DataFrame
    traces = []
    for speed_bin in vind_hastighet:
        traces.append(go.Barpolar(
            r=df['speed_bin'].tolist(),
            theta=df['direction_bin'].tolist(),
            name=speed_bin,
            marker_line_color="black",
            marker_line_width=0.5,
            opacity=0.8
        ))
    layout = {
        'title': 'Vindrose',
        'font': {
            'size': 16
        },
        'polar': {
            'radialaxis': {
                'ticksuffix': '%',
            },
            'angularaxis': {
                'direction' : 'clockwise',
                'rotation' : 90
            }
        }
    }
    # Convert traces to JSON
    traces_json = json.dumps([trace.to_plotly_json() for trace in traces])
    return {'data': traces_json, 'layout': layout}

def scatter_plot(request):
    # Create a scatter plot
    fig = go.Figure(data=go.Scatter(x=[1, 2, 3, 4], y=[10, 15, 13, 17], mode='markers'))

    # Convert the figure to JSON
    fig_json = json.loads(fig.to_json())

    # Send the JSON to the front end
    return fig_json

def vindrose_stasjon(stasjonsid, dager_tidligere):
    df = vindrose(stasjonsid, dager_tidligere)
    vind_hastighet = ['0-4 m/s', '4-8 m/s', '8-11 m/s', '11-14 m/s', '14-17 m/s', '17-20 m/s', '20-25 m/s', '>25 m/s']
    colors = ['#482878', '#3e4989', '#31688e', '#26828e', '#1f9e89', '#35b779', '#6ece58', '#b5de2b']
    direction_to_degrees = {
    'N': 0,
    'NØ': 45,
    'Ø': 90,
    'SØ': 135,
    'S': 180,
    'SV': 225,
    'V': 270,
    'NV': 315
    }
    theta = [direction_to_degrees[dir_bin]-45 for dir_bin in df.index]
    print(theta)
    fig = go.Figure()
    for i, hastighet in enumerate(vind_hastighet):
        fig.add_trace(go.Barpolar(
            r=df[hastighet].tolist(),
            theta=theta,
            name=hastighet,
            marker_color=colors[i],
        ))

    
    fig.update_traces(text=['N-V','Nord','N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'])
    fig.update_layout(
        title='Wind Speed Distribution in Laurel, NE',
        font_size=16,
        legend_font_size=16,
        polar_radialaxis_ticksuffix='%',
        polar_angularaxis_rotation=90,
        polar_angularaxis_direction='clockwise',

    )
    

    return fig