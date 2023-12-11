from django.shortcuts import render
from django.http import HttpResponse
from .apidata.snowsense import hent_snowsense
from .apidata.stasjon import hent_frost
from .apidata.vaerplot import vaerplot, frostplot

værstasjoner = {
    58705: {'eigar': 'SVV', 'navn':'Rv15 Strynefjell - Kvitenova', 'lat': 61.988, 'lon': 7.330, 'altitude': 1422},
    58703: {'eigar': 'SVV', 'navn':'Rv15 Skjerdingsdalen', 'lat':61.9633, 'lon': 7.254, 'altitude': 590},
    15951: {'eigar': 'SVV', 'navn':'Rv15 Breidalen II', 'lat': 62.0103, 'lon': 7.392, 'altitude': 929},
}

andre_stasjoner = {
    'Stavbrekka': {'stasjonstype':'Snowsense', 'lat':62.0176, 'lon':7.375, 'altitude':1300}
}
# Create your views here.
def index(request):
    snowsense_data = hent_snowsense()

    # Get weather data
    graph1 = vaerplot(værstasjoner[58705]['lat'], værstasjoner[58705]['lon'], navn=værstasjoner[58705]['navn'], altitude=værstasjoner[58705]['altitude'], stasjonsid=58705, elements=['air_temperature'])
    graph2 = vaerplot(værstasjoner[58703]['lat'], værstasjoner[58703]['lon'], navn=værstasjoner[58703]['navn'], altitude=værstasjoner[58703]['altitude'], stasjonsid=58703, elements=['air_temperature', 'sum(precipitation_amount PT10M)', 'wind_speed'])

    return render(request, 'vaerdata/datavisning.html', {
        'graph1': graph1,
        'graph2': graph2,
        'snowsense_data': snowsense_data}
        )


def test(request):
    return HttpResponse("Hello, world. Test varsling")