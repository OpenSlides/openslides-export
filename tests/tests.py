# -*- coding: utf-8 -*-

import datetime
import time

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test.client import Client

from openslides.agenda.models import Item, Speaker
from openslides.participant.models import User
from openslides.utils.test import TestCase


class CSVExportView(TestCase):
    """
    Tests the export view and its output, the csv file.
    """
    def setUp(self):
        ct = ContentType.objects.get(app_label='openslides_export', model='export')
        perm = Permission.objects.get(content_type=ct, codename='can_export')
        self.manager = User.objects.create_user(username='AhxahShahGeb7eith8ua', password='Theithooxa9no0ahgae0')
        self.manager.user_permissions.add(perm)
        self.normal_user = User.objects.create_user(username='Theithooxa9no0ahgae0', password='Ohai4aeyo7can1fahzat')
        self.client_1 = Client()
        self.client_1.login(username='AhxahShahGeb7eith8ua', password='Theithooxa9no0ahgae0')
        self.client_2 = Client()
        self.client_2.login(username='Theithooxa9no0ahgae0', password='Ohai4aeyo7can1fahzat')

    def test_get_manager(self):
        response = self.client_1.get('/export/agenda/speakers/')
        self.assertContains(response, 'Item,Person,Begin Time,End Time', status_code=200)

    def test_get_normal_user(self):
        response = self.client_2.get('/export/agenda/speakers/')
        self.assertEqual(response.status_code, 403)

    def test_csv_content(self):
        item1 = Item.objects.create(title='Iangohse5pae7eineeca')
        speaker1 = Speaker.objects.add(self.manager, item1)
        response = self.client_1.get('/export/agenda/speakers/')
        self.assertContains(response, 'Iangohse5pae7eineeca,AhxahShahGeb7eith8ua,', status_code=200)
        speaker1.begin_speach()
        response = self.client_1.get('/export/agenda/speakers/')
        text = 'Iangohse5pae7eineeca,AhxahShahGeb7eith8ua,%s' % datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        self.assertContains(response, text, status_code=200)
        time.sleep(1)
        speaker1.end_speach()
        response = self.client_1.get('/export/agenda/speakers/')
        text = '%s,%s' % (text, datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
        self.assertContains(response, text, status_code=200)

    def test_main_menu(self):
        response = self.client_1.get('/dashboard/')
        self.assertContains(response, 'Export', status_code=200)
        response = self.client_2.get('/dashboard/')
        self.assertNotContains(response, 'Export', status_code=200)
