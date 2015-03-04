Instruction to update translation for this plugin:
--------------------------------------------------

1. Go to the plugin directory (which contains the 'locale' directory):
   $ cd openslides_export

2. Update the German po file (locale/de/LC_MESSAGES/django.po):
   $ django-admin.py makemessages -l de

3. Edit the German po file
   (Search for "fuzzy" and empty msgstr entries.)

4. Update the German mo file (locale/de/LC_MESSAGES/django.mo):
   $ django-admin.py compilemessages

5. Restart server:
   $ python manage.py runserver

--
Additional hints for internationalization (i18n) in Django:
https://docs.djangoproject.com/en/dev/topics/i18n/

Note: gettext is required to extract message IDs or compile message files.
For gettext on Windows read:
https://docs.djangoproject.com/en/dev/topics/i18n/translation/#gettext-on-windows
