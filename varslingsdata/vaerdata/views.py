from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .apidata.snowsense import hent_snowsense
from .apidata.stasjon import hent_frost, vindrose
from .apidata.vaerplot import vaerplot, frostplot_temp_nedbør_snø, met_plot, frostplot_vind, frost_windrose, windrose_test, windrose_test2, scatter_plot, vindrose_stasjon
import json

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
    yrsvg1 = 'https://www.yr.no/nb/innhold/1-2205713/meteogram.svg'  #Kvitenova
    yrsvg2 = 'https://www.yr.no/nb/innhold/1-169829/meteogram.svg'

    return render(request, 'vaerdata/vaerdata.html', {
        'yrsvg1': yrsvg1,
        'yrsvg2': yrsvg2,})

def index_gammel(request):
    yrsvg1 = 'https://www.yr.no/nb/innhold/1-2205713/meteogram.svg'  #Kvitenova
    yrsvg2 = 'https://www.yr.no/nb/innhold/1-169829/meteogram.svg'

    return render(request, 'vaerdata/datavisning.html', {
        'yrsvg1': yrsvg1,
        'yrsvg2': yrsvg2,})

def get_snowsense(request):
    snowsense_data = hent_snowsense()
    print(snowsense_data)
    #graph1 = vaerplot(værstasjoner[58705]['lat'], værstasjoner[58705]['lon'], navn=værstasjoner[58705]['navn'], altitude=værstasjoner[58705]['altitude'], stasjonsid=58705, elements=['air_temperature'])
    #graph2 = vaerplot(værstasjoner[58703]['lat'], værstasjoner[58703]['lon'], navn=værstasjoner[58703]['navn'], altitude=værstasjoner[58703]['altitude'], stasjonerid=58703, elements=['air_temperature', 'sum(precipitation_amount PT10M)', 'wind_speed'])
    return JsonResponse({
        'snowsense_data': snowsense_data
    })

def vaer(request):
    vaerplot_graf = vaerplot(værstasjoner[58703]['lat'], værstasjoner[58703]['lon'], værstasjoner[58703]['navn'], værstasjoner[58703]['altitude'], 58703, værstasjoner[58703]['elements'])
    return JsonResponse({
        'vaerplot_graf': vaerplot_graf
    })

def get_graph1(request):
    fig = met_plot(værstasjoner[58703]['lat'], værstasjoner[58703]['lon'], navn=værstasjoner[58703]['navn'], altitude=værstasjoner[58703]['altitude'])
    
    fig_json = json.loads(fig.to_json())

    return JsonResponse({
        'fig_json': fig_json
    })


def get_graph2(request):
    graph2 = frostplot_temp_nedbør_snø(58703, 20, værstasjoner[58703]['elements'])

    return JsonResponse({
        'graph2': graph2
    })

def get_graph3(request):
    graph3 = frostplot_vind(58703, 20, værstasjoner[58703]['elements'])

    return JsonResponse({
        'graph3': graph3
    })

def get_windrose(request):
    windrose = windrose_test()

    return JsonResponse({
        'windrose': windrose
    })

def get_windrose2(request):
    df_wind_speed, df_wind_from_direction = vindrose(58703, 5)

    return JsonResponse({
        'wind_speed': df_wind_speed.to_json(),
        'wind_from_direction': df_wind_from_direction.to_json()

    })

def get_windrose3(request):
    vindrose = windrose_test2(58703, 5)

    return JsonResponse({
        'vindrose': vindrose
    })


def lag_graf(request):
    graf = scatter_plot(request)

    return JsonResponse({
        'graf': graf
    })

def test(request):
    return HttpResponse("Hello, world. Test varsling")

def vindrose_stasjon_data(request):
    fig = vindrose_stasjon(58705, dager_tidligere=1)
    
    fig_json = json.loads(fig.to_json())

    return JsonResponse({
        'fig_json': fig_json
    })

