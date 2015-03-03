# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^export/$',
        views.ExportListView.as_view(),
        name='export_list'),
    url(r'^export/speakers/$',
        views.ExportSpeakersView.as_view(),
        name='export_speakers'),
    url(r'^export/motion/(?P<pk>\w+)/(?P<format>\w+)$',
        views.ExportMotionView.as_view(),
        name='export_motion'))
