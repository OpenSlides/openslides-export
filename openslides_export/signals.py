# -*- coding: utf-8 -*-

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver

from openslides.core.signals import post_database_setup
from openslides.participant.models import Group


@receiver(post_database_setup, dispatch_uid='openslides_export_add_permission')
def openslides_export_add_permission(sender, **kwargs):
    """
    Adds the export permission the the builtin staff group.
    """
    try:
        group_staff = Group.objects.get(name='Staff', pk=4)
    except Group.DoesNotExist:
        # Do not add the export permission
        pass
    else:
        perm = Permission.objects.get(
            content_type=ContentType.objects.get(
                app_label='openslides_export',
                model='export'),
            codename='can_export')
        group_staff.permissions.add(perm)
