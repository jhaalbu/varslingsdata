import plotly.graph_objects as go
import plotly.io as pio
import plotly.utils as pu
from metno_locationforecast import Place, Forecast
from .met import metno_temperatur, metno_nedbør
from .stasjon import hent_frost
import json

def vaerplot(lat, lon, navn, altitude, stasjonsid, elements):
    user_agent = "Stedspesifikk v/0.1 jan.helge.aalbu@vegvesen.no"
    vaer = Place(navn, lat, lon, altitude)
    vaer_forecast = Forecast(vaer, user_agent)
    vaer_forecast.update()
    time_nebør, nedbør = metno_nedbør(vaer_forecast)
    time_temperatur, temperatur = metno_temperatur(vaer_forecast)

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

def frostplot(stasjonsid, dager):
    df = hent_frost(stasjonsid, dager_tidligere=dager, elements='air_temperature', timeoffsets='PT0H')

    fig = go.Figure()
    #fig.add_trace(go.Bar(x=time_nebør, y=nedbør, name='nedbør', width=1000 * 3600 * 5))
    fig.add_trace(go.Scatter(x=df['referenceTime'], y=df['value'], mode='lines', name='temperatur'))

    # Convert the graph to JSON format
    return json.dumps(fig, cls=pu.PlotlyJSONEncoder)