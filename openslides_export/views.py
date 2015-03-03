# -*- coding: utf-8 -*-

from cStringIO import StringIO
import csv
import os
from openslides.global_settings import *

from django.http import HttpResponse
from django.utils.translation import ugettext as _

from py3o.template import Template as TemplatePy3o

from openslides.agenda.models import Speaker
from openslides.config.api import config
from openslides.motion.models import Motion
from openslides.utils.views import PermissionMixin, DetailView, TemplateView, View


class ExportListView(TemplateView):
    """
    View of the overview page of all exportable elements
    """
    template_name = 'openslides_export/export_list.html'

    def get_context_data(self, *args, **kwargs):
        """
        Inserts all agenda items into the context.
        """
        context = super(ExportListView, self).get_context_data(*args, **kwargs)
        context['motions'] = Motion.objects.all()
        return context


class ExportSpeakersView(PermissionMixin, View):
    """
    View to export the lists of speakers of all agenda items as CSV.
    """

    def get(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename=list_of_speakers.csv;'
        csv_writer = csv.writer(response)
        csv_writer.writerow(['Item', 'Person', 'Begin Time', 'End Time'])
        for speaker in Speaker.objects.all().order_by('item', 'weight', 'begin_time'):
            try:
                begin_time = speaker.begin_time.strftime('%d.%m.%Y %H:%M:%S')
            except AttributeError:
                begin_time = None
            try:
                end_time = speaker.end_time.strftime('%d.%m.%Y %H:%M:%S')
            except AttributeError:
                end_time = None
            csv_writer.writerow([
                speaker.item.get_title().encode('utf8'), unicode(speaker.person).encode('utf8'), begin_time, end_time])
        return response


class ExportMotionView(DetailView):
    """
    View to export a motion or a list of motions as ODT.
    """
    filename = None
    odt_template = None
    model = Motion

    def get_object(self, *args, **kwargs):
        try:
            obj = super(ExportMotionView, self).get_object(*args, **kwargs)
        except ValueError:
            obj = None
        return obj

    def get_format(self):
        """
        Return the selected export format.
        """
        return self.kwargs.get('format', 'odt')

    def get(self, request, *args, **kwargs):
        return self.render_to_response()

    def get_filename(self):
        """
        Return the filename for the output file (without suffix).
        """
        motion = self.get_object()
        if motion:
            filename = "%s-%s" % (_("Motion"), motion.identifier)
        else:
            filename = _("Motion-list")
        return filename

    def get_odt_template(self):
        """
        Return the path to the odt template file.
        """
        if self.get_object():
            odt_template = os.path.join(SITE_ROOT, '../openslides_export/templates/openslides_export/template-motion.odt')
        else:
            odt_template = os.path.join(SITE_ROOT, '../openslides_export/templates/openslides_export/template-motion-list.odt')
        return odt_template

    def get_variables(self):
        return dict({
            'event_name': config['event_name'],
            'event_description': config['event_description'],
            'event_date': config['event_date'],
            'motion': self.get_object(),
            'motions': Motion.objects.all(),
        })

    def render_to_response(self):
        response = HttpResponse(content_type='application/vnd.oasis.opendocument.text')
        filename = u'filename=%s.odt;' % self.get_filename()
        response['Content-Disposition'] = filename.encode('utf-8')

        buffer = StringIO()
        odt_template = self.get_odt_template()
        template = TemplatePy3o(odt_template, buffer, ignore_undefined_variables=True)
        variables = self.get_variables()
        template.render(variables)
        odt_output = buffer.getvalue()
        buffer.close()
        response.write(odt_output)
        return response