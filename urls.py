__author__ = 'faebser'

from django.shortcuts import render
from django.conf.urls import url, patterns
import views
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    url(r'^tags/(?P<tag>[\w\#0-9]+)/$', views.get_list_from_tag, name="tag"),
    url(r'^author/(?P<firstname>[\w]+)-(?P<lastname>[\w]+)/$', views.get_list_from_author, name="person")
]