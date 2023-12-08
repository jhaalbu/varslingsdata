from django.shortcuts import render
from django.http import HttpResponse
from .apidata.snowsense import hent_snowsense

# Create your views here.
def index(request):
    # Hent data fra snowsense
    snowsense_data = hent_snowsense()
    return render(request, 'datavisning.html', {'data': data, 'chart_data': chart_data})