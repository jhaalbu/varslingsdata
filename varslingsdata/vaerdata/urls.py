from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("gammel/", views.index_gammel, name="index_gammel"),
    path("test/", views.test, name="test"),
    path("get_snowsense/", views.get_snowsense, name="get_snowsense"),
    path("get_graph1/", views.get_graph1, name="get_graph1"),
    path("get_graph2/", views.get_graph2, name="get_graph2"),
    path("get_graph3/", views.get_graph3, name="get_graph3"),
    path("get_windrose/", views.get_windrose, name="get_windrose"),
    path("get_windrose2/", views.get_windrose2, name="get_windrose2"),
    path("get_windrose3/", views.get_windrose3, name="get_windrose3"),
    path("lag_graf/", views.lag_graf, name="lag_graf"),
    path("vaer/", views.vaer, name="vaer"),
    path("vindrose_stasjon_data/", views.vindrose_stasjon_data, name="vindrose_stasjon_data"),
    
]