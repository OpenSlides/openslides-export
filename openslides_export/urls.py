# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^export/$',
        views.ExportListView.as_view(),
        name='export_list'),
    url(r'^export/agenda/full$',
        views.ExportAgendaView.as_view(),
        name='export_agenda'),
    url(r'^export/agenda/speakers/$',
        views.ExportAgendaSpeakersView.as_view(),
        name='export_agenda_speakers'),
    url(r'^export/motion/(?P<pk>\w+)/(?P<format>\w+)$',
        views.ExportMotionView.as_view(),
        name='export_motion'))
