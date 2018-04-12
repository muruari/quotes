from django.conf.urls import url
from . import views

urlpatterns = [
   
    url(r'^$', views.registration),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^create_quote$', views.create_quote),
    url(r'^add_quote/(?P<id>\d+)$', views.add_quote),
    url(r'^remove_quote/(?P<id>\d+)$', views.remove_quote),
    url(r'^quote/(?P<id>\d+)$', views.quote_info),
    url(r'^dashboard$', views.dashboard)
       
]