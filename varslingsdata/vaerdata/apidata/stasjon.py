import json
from .frost2df import frost2df, obs2df
from datetime import datetime, timedelta
from dateutil import parser, tz
import pandas as pd
import numpy as np


def frost_api(stasjonsid, dager_tidligere, element, timeoffsets='PT0H'):
    now = datetime.now().replace(minute=0, second=0, microsecond=0)

    #Finner tidspunkt for xx dager siden
    earlier_date = now - timedelta(days=dager_tidligere)

    # Konverterer til string
    now_str = now.isoformat()
    earlier_date_str = earlier_date.isoformat()
    parameters = {
    'sources':'SN' + str(stasjonsid),
    'elements': element,
    'referencetime': earlier_date_str + '/' + now_str,
    'timeoffsets': timeoffsets
    }

    df = obs2df(parameters=parameters, verbose=True)
    df['referenceTime'] = df['referenceTime'].dt.tz_localize(None)
    df.set_index('referenceTime', inplace=True)
    df.sort_index(inplace=True)
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    return df


def hent_frost(stasjonsid, dager_tidligere, element, timeoffsets='PT0H'):
    '''Funksjon som henter data fra frost.met.no og returnerer en liste med data for en gitt stasjon.
    Funksjonen henter data fra frost.met.no. Den bruker frost2df for å håndtere apikall.

    Args:
        stasjonsid (int): Stasjonsid for stasjonen du vil hente data for.
        dager_tidligere (int): Antall dager du vil hente data for.
        elements (list): Liste med elementer du vil hente data for.
        timeoffsets (str): Tidsoffset for dataene.
    
    Returns:
        dataframe: Dataframe med data for en gitt stasjon.
    '''
    df = frost_api(stasjonsid, dager_tidligere, element, timeoffsets)
    # Resample to hourly frequency
    df_hourly = df.resample('H')
    

    # Resample to hourly frequency and calculate the mean or sum
    if element in ['air_temperature', 'surface_snow_thickness', 'wind_speed', 'wind_from_direction']:
        df_hourly = df['value'].resample('H').mean().to_frame()
    elif element == 'sum(precipitation_amount PT10M)':
        df_hourly = df['value'].resample('H').sum().to_frame()

    df_hourly.reset_index(inplace=True)
    df_hourly['value'] = df_hourly['value'].replace({np.nan: None})
    return df_hourly['referenceTime'].to_list(), df_hourly['value'].to_list()

def vindrose(stasjonsid, dager_tidligere):
    df_wind_speed = frost_api(stasjonsid, dager_tidligere, element='wind_speed', timeoffsets='PT0H')
    df_wind_from_direction = frost_api(stasjonsid, dager_tidligere, element='wind_from_direction', timeoffsets='PT0H')

    bin_edges = [337.5, 22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]
    bin_labels = ['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W']


    # Assign each wind direction to a bin
    df_wind_from_direction['direction_bin'] = pd.cut(df_wind_from_direction['value'], bins=bin_edges, labels=bin_labels, right=False)

    # Calculate the frequency of each bin
    frequency_df = df_wind_from_direction['direction_bin'].value_counts().reindex(bin_labels).fillna(0)

    # Convert the frequency series to a dataframe
    frequency_df = frequency_df.reset_index()
    frequency_df.columns = ['Direction', 'Frequency']
    print(df_wind_from_direction)
    print(frequency_df)
    return df_wind_speed, frequency_df


    