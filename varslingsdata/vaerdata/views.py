from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .apidata.snowsense import hent_snowsense
from .apidata.stasjon import hent_frost
from .apidata.vaerplot import vaerplot, frostplot_temp_nedbør_snø, met_plot

værstasjoner = {
    58705: {'eigar': 'SVV', 
            'navn':'Rv15 Strynefjell - Kvitenova', 
            'lat': 61.988, 'lon': 7.330, 
            'altitude': 1422, 
            'elements': [
                'air_temperature', 
                'wind_from_direction', 
                'wind_speed']},
    58703: {'eigar': 'SVV', 
            'navn':'Rv15 Skjerdingsdalen', 
            'lat':61.9633, 'lon': 7.254, 
            'altitude': 590,
            'elements': [
                'air_temperature', 
                'sum(precipitation_amount PT10M)', 
                'wind_speed',
                'wind_from_direction',
                'surface_snow_thickness',
                'accumulated(precipitation_amount)',
                ]},
    15951: {'eigar': 'SVV', 
            'navn':'Rv15 Breidalen II', 
            'lat': 62.0103, 'lon': 7.392, 
            'altitude': 929,
            'elements': [
                'air_temperature', 
                'sum(precipitation_amount PT10M)', 
                'wind_speed',
                'wind_from_direction',
                'surface_snow_thickness',
                'accumulated(precipitation_amount)',
                ]},
}

andre_stasjoner = {
    'Stavbrekka': {'stasjonstype':'Snowsense', 'lat':62.0176, 'lon':7.375, 'altitude':1300}
}
# Create your views here.
def index(request):
    return render(request, 'vaerdata/datavisning.html')

def get_snowsense(request):
    snowsense_data = hent_snowsense()
    print(snowsense_data)
    #graph1 = vaerplot(værstasjoner[58705]['lat'], værstasjoner[58705]['lon'], navn=værstasjoner[58705]['navn'], altitude=værstasjoner[58705]['altitude'], stasjonsid=58705, elements=['air_temperature'])
    #graph2 = vaerplot(værstasjoner[58703]['lat'], værstasjoner[58703]['lon'], navn=værstasjoner[58703]['navn'], altitude=værstasjoner[58703]['altitude'], stasjonerid=58703, elements=['air_temperature', 'sum(precipitation_amount PT10M)', 'wind_speed'])
    return JsonResponse({
        'snowsense_data': snowsense_data
    })

def get_graph1(request):
    graph1 = met_plot(værstasjoner[58703]['lat'], værstasjoner[58703]['lon'], navn=værstasjoner[58703]['navn'], altitude=værstasjoner[58703]['altitude'])
    
    return JsonResponse({
        'graph1': graph1
    })

def get_graph2(request):
    graph2 = frostplot_temp_nedbør_snø(58703, 20, værstasjoner[58703]['elements'])

    return JsonResponse({
        'graph2': graph2
    })

def test(request):
    return HttpResponse("Hello, world. Test varsling")