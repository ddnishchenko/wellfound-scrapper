from django.urls import path

from . import views

app_name = 'scrapper'
urlpatterns = [
    path('', views.index, name='index'),
]