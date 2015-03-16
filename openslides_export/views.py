# -*- coding: utf-8 -*-

from cStringIO import StringIO
import csv
import os
import re

from genshi.core import Markup

from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template
from django.utils.translation import ugettext as _

from py3o.template import Template as TemplatePy3o

from openslides.agenda.models import Item, Speaker
from openslides.config.api import config
from openslides.motion.models import Motion
from openslides.utils.views import PermissionMixin, DetailView, TemplateView, View


class ExportListView(TemplateView):
    """
    View of the overview page of all exportable elements
    """
    template_name = 'openslides_export/export_list.html'
    required_permission = 'openslides_export.can_export'

    def get_context_data(self, *args, **kwargs):
        """
        Inserts all agenda items into the context.
        """
        context = super(ExportListView, self).get_context_data(*args, **kwargs)
        context['motions'] = Motion.objects.all()
        return context


class ExportAgendaView(PermissionMixin, View):
    """
    View to export the agenda as CSV.
    """
    required_permission = 'openslides_export.can_export'

    def get(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Content-Disposition'] = 'attachment; filename=agenda.csv;'
        csv_writer = csv.writer(response)
        csv_writer.writerow(['Title', 'Text', 'Duration'])
        for item in Item.objects.all():
            csv_writer.writerow([
                item, item.text.encode('utf8'), item.duration])
        return response


class ExportAgendaSpeakersView(PermissionMixin, View):
    """
    View to export the lists of speakers of all agenda items as CSV.
    """
    required_permission = 'openslides_export.can_export'

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


class ExportMotionODTView(DetailView):
    """
    View to export a motion or a list of motions as ODT.
    """
    required_permission = 'openslides_export.can_export'
    filename = None
    odt_template = None
    model = Motion

    def get_object(self, *args, **kwargs):
        try:
            obj = super(ExportMotionODTView, self).get_object(*args, **kwargs)
        except ValueError:
            obj = None
        return obj

    def get(self, request, *args, **kwargs):
        return self.render_to_response()

    def get_filename(self):
        """
        Return the filename for the output file (without suffix).
        """
        motion = self.get_object()
        if motion:
            if motion.identifier:
                filename = "%s-%s" % (_("Motion"), motion.identifier)
            else:
                filename = "%s" % (_("Motion"))
        else:
            filename = _("Motion-list")
        return filename

    def get_odt_template(self):
        """
        Return the path to the odt template file.
        """
        if self.get_object():
            odt_template = os.path.join(os.path.dirname(__file__), 'templates', 'openslides_export', 'template-motion.odt')
        else:
            odt_template = os.path.join(os.path.dirname(__file__), 'templates', 'openslides_export', 'template-motion-list.odt')
        return odt_template

    def format_py3o_context_value(self, value):
        # remove html tags and replace all linebreaks
        return Markup(unicode(re.sub('<.*?>', '', value)).replace('\n', '<text:line-break/>'))

    def get_variables(self):
        motion = self.get_object()
        text = None
        reason = None
        if motion:
            text = self.format_py3o_context_value(motion.text)
            reason = self.format_py3o_context_value(motion.reason)

        return dict({
            'event_name': config['event_name'],
            'event_description': config['event_description'],
            'event_date': config['event_date'],
            'motion': motion,
            'text': text,
            'reason': reason,
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


class ExportMotionHTMLView(DetailView):
    """
    View to export a motion or a list of motions as HTML.
    """
    required_permission = 'openslides_export.can_export'
    filename = None
    html_template = None
    model = Motion

    def get_object(self, *args, **kwargs):
        try:
            obj = super(ExportMotionHTMLView, self).get_object(*args, **kwargs)
        except ValueError:
            obj = None
        return obj

    def get_filename(self):
        """
        Return the filename for the output file (without suffix).
        """
        motion = self.get_object()
        if motion:
            if motion.identifier:
                filename = "%s-%s" % (_("Motion"), motion.identifier)
            else:
                filename = "%s" % (_("Motion"))
        else:
            filename = _("Motion-list")
        return filename

    def get_html_template(self):
        """
        Return the path to the odt template file.
        """
        if self.get_object():
            html_template = get_template('openslides_export/template-motion.html')
        else:
            html_template = get_template('openslides_export/template-motion-list.html')
        return html_template

    def get(self, *args, **kwargs):
        """
        Renders the selected motion with the template as HTML
        """
        context = RequestContext(
            self.request,
            {'motion': self.get_object(),
             'motions': Motion.objects.all()}
        )
        response = HttpResponse(self.get_html_template().render(context), content_type="text/html")
        filename = u'filename=%s.html;' % self.get_filename()
        response['Content-Disposition'] = filename.encode('utf-8')
        return response
