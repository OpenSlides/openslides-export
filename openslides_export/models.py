# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_noop


class Export(models.Model):
    """
    The (empty) export model for define export permission.
    """

    class Meta:
        permissions = (('can_export', ugettext_noop('Can export data')),)
