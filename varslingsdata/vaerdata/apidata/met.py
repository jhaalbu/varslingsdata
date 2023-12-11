

def metno_temperatur(metno_forecst):
    tidspunkt_temp = []
    temperatur = []
    for i in metno_forecst.data.intervals:
        try:
            temperatur.append(i.variables['air_temperature'].value)
            tidspunkt_temp.append(i.start_time)
        except:
            continue
    return tidspunkt_temp, temperatur

def metno_nedbør(metno_forecst):
    tidspunkt_nedbor = []
    nedbor = []
    for i in metno_forecst.data.intervals:
        try:
            nedbor.append(i.variables['precipitation_amount'].value)
            tidspunkt_nedbor.append(i.start_time)
        except:
            continue
    return tidspunkt_nedbor, nedbor

