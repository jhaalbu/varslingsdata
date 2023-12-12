import plotly.graph_objects as go
import plotly.io as pio
import plotly.utils as pu
from metno_locationforecast import Place, Forecast
from .met import metno_temperatur, metno_nedbør
from .stasjon import hent_frost
import json
from datetime import datetime, timedelta
from dateutil.parser import parse
import numpy as np

def vaerplot(lat, lon, navn, altitude, stasjonsid, elements):
    user_agent = "Stedspesifikk v/0.1 jan.helge.aalbu@vegvesen.no"
    vaer = Place(navn, lat, lon, altitude)
    vaer_forecast = Forecast(vaer, user_agent)
    vaer_forecast.update()
    time_nebør, nedbør = metno_nedbør(vaer_forecast)
    #print(nedbør)
    time_temperatur, temperatur = metno_temperatur(vaer_forecast)

    line_elements = ['air_temperature', 'wind_speed']
    bar_elements = ['sum(precipitation_amount PT10M)']


    # Lager til figuren
    fig = go.Figure()

    #Plotter ut data fra yr apiet
    fig.add_trace(go.Bar(x=time_nebør, y=nedbør, name='Nedbør (YR)', width=1000 * 3600 * 5, yaxis='y2'))
    fig.add_trace(go.Scatter(x=time_temperatur, y=temperatur, mode='lines', name='temperatur (YR)'))
    
    #Henter ut data fra forst apiet
    værhist = hent_frost(stasjonsid, elements, dager_tidligere=5, timeoffsets='PT0H')

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
        )
    )

    # Convert the graph to JSON format
    return json.dumps(fig, cls=pu.PlotlyJSONEncoder)

def met_plot(lat, lon, navn, altitude, dager=4):
    user_agent = "Stedspesifikk v/0.1 jan.helge.aalbu@vegvesen.no"
    vaer = Place(navn, lat, lon, altitude)
    vaer_forecast = Forecast(vaer, user_agent)
    vaer_forecast.update()
    time_nebør, nedbør = metno_nedbør(vaer_forecast, dager)

    time_temperatur, temperatur = metno_temperatur(vaer_forecast, dager)

    nedbør_cumsum = np.cumsum(nedbør).tolist()

    trace_nedbør_cumsum = {
        'x': time_nebør,
        'y': nedbør_cumsum,
        'type': 'scatter',
        'name': 'Kumulativ nedbør',
        'fill': 'tozeroy',
        'fillcolor': 'rgba(0, 0, 255, 0.1)', 
        'yaxis': 'y3',
    }

    trace_nedbør = {
        'x': time_nebør,
        'y': nedbør,
        'type': 'bar',
        'name': 'Nedbør',
        'width': 500 * 3600 * (dager/2),
        'yaxis': 'y2',
 
    }
    trace_temperatur = {
        'x': time_temperatur,
        'y': temperatur,
        'type': 'scatter',
        'name': 'Temperatur',
        'marker': {'color': 'red'},
    }
    traces = [trace_nedbør_cumsum, trace_nedbør, trace_temperatur]

    layout = {
        'yaxis2': {
            'title': 'Nedbør',
            'overlaying': 'y',
            'side': 'right',
            'showgrid': False,  # Hide the grid lines
            'range': [min(nedbør_cumsum), max(nedbør_cumsum)]  # Set the same range as yaxis3
        },
        'yaxis': {
            'title': 'Temperatur',
            'showgrid': False,  # Hide the grid lines
        },
        'yaxis3': {  # Add a second y-axis
            'title': 'Nedbør',
            'overlaying': 'y',
            'side': 'right',
            'showgrid': False,  # Hide the grid lines
            'zeroline': False,  # Hide the zero line
            'range': [min(nedbør_cumsum), max(nedbør_cumsum)]  # Set the range based on your data
        },
    }
    return {'data': traces, 'layout': layout}

def frostplot_temp_nedbør_snø(stasjonsid, dager, elements):
    traces = []
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
            'yaxis': 'y3'
            }
            traces.append(trace)

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
        },
        'xaxis': {'domain': [0.0, 0.8]},
    }
    return {'data' : traces, 'layout': layout}

def samleplot(plotjson):
    return
