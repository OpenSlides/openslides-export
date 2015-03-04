# -*- coding: utf-8 -*-

from openslides.utils.main_menu import MainMenuEntry


class ExportPluginMainMenuEntry(MainMenuEntry):
    """
    Main menu entry for OpenSlides Export Plugin.
    """
    verbose_name = 'Export'
    required_permission = 'openslides_export.can_export'
    default_weight = 100
    pattern_name = 'export_list'
    icon_css_class = 'icon-export'
    stylesheets = ['css/openslides_export.css']
