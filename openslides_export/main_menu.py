# -*- coding: utf-8 -*-

from openslides.utils.main_menu import MainMenuEntry


class ExportPluginMainMenuEntry(MainMenuEntry):
    """
    Main menu entry for OpenSlides Export Plugin.
    """
    verbose_name = 'Export'
    required_permission = 'motion.can_manage_motion'
    default_weight = 100
    pattern_name = 'export_list'
    icon_css_class = 'icon-export'
    stylesheets = ['css/openslides_export.css']
