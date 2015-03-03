==========================
 OpenSlides Export Plugin
==========================

Overview
========

This plugin for OpenSlides provides a odt/csv export of OpenSlides data
(e.g. motions and agenda).


Requirements
============

- OpenSlides 1.7.x (http://openslides.org/)
- py3o.template (for odt export)
see requirements.txt

Install
=======

This is only an example instruction to install the plugin on GNU/Linux. It
can also be installed as any other python package and on other platforms,
e. g. on Windows.

Change to a new directory::

    $ cd

    $ mkdir OpenSlides

    $ cd OpenSlides

Setup and activate a virtual environment and install OpenSlides and the
plugin in it::

    $ virtualenv .virtualenv

    $ source .virtualenv/bin/activate

    $ pip install "openslides>=1.7,<1.8" openslides-export

Start OpenSlides::

    $ openslides


License and authors
===================

This plugin is Free/Libre Open Source Software and distributed under the
MIT License, see LICENSE file. The authors are mentioned in the AUTHORS file.


Changelog
=========


Version 1.0 (unreleased)
------------------------
* First release of this plugin.
