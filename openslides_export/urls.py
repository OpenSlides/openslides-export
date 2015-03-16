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
    url(r'^export/motion/(?P<pk>\w+)/odt$',
        views.ExportMotionODTView.as_view(),
        name='export_motion_odt'),
    url(r'^export/motion/(?P<pk>\w+)/html$',
        views.ExportMotionHTMLView.as_view(),
        name='export_motion_html'))
