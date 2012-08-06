# -*- coding: utf-8 -*-
"""
URL dispatcher config for Pagetags Django CMS plugin.
"""
from django.conf.urls import patterns, include, url

from pagetags import views


urlpatterns = patterns('',
    url(r'^$', views.list_tags),
)
