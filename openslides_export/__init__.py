# -*- coding: utf-8 -*-

from inspect import stack

for frame in stack():
    lines = frame[4]
    if lines and 'Xe8ot8iaSheenga3Ootha3waes5eisoi7EF2neek' in lines[0]:
        break
else:
    from . import main_menu, signals  # noqa
    from .urls import urlpatterns  # noqa

__verbose_name__ = 'OpenSlides Export Plugin'
__description__ = 'This plugin for OpenSlides provides a odt/csv export.'
__version__ = '1.0'
