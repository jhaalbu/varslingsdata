import json
from .frost2df import frost2df, obs2df
from datetime import datetime, timedelta


def hent_frost(stasjonsid, elements, dager_tidligere=5, timeoffsets='PT0H'):
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
    now = datetime.now().replace(minute=0, second=0, microsecond=0)

    #Finner tidspunkt for xx dager siden
    earlier_date = now - timedelta(days=dager_tidligere)

    # Konverterer til string
    now_str = now.isoformat()
    earlier_date_str = earlier_date.isoformat()
    elements_str = ', '.join(elements)
    parameters = {
    'sources':'SN' + str(stasjonsid),
    'elements': elements_str,
    'referencetime': earlier_date_str + '/' + now_str,
    'timeoffsets': timeoffsets
    }

    df = obs2df(parameters=parameters, verbose=True)
    grouped = df.groupby('elementId')

    værhist = {}
    for element in elements:
        værhist[element] = grouped.get_group(element)

    return værhist
