from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.test, name="test"),
    path("get_snowsense/", views.get_snowsense, name="get_snowsense"),
    path("get_graph1/", views.get_graph1, name="get_graph1"),
    path("get_graph2/", views.get_graph2, name="get_graph2"),
]