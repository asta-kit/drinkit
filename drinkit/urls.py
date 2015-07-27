from django.conf.urls import url

from . import views

app_name = 'drinkit'
urlpatterns = [
    url('^strichliste$', views.tally_sheet, name='tally_sheet')
]
