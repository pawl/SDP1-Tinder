import re
import os

from django.utils.translation import ugettext_lazy as _

from django.core.validators import RegexValidator

AlphaRegexValidator = RegexValidator(regex=re.compile(r'^[\w\s]*$', flags=re.UNICODE), message=_('Only letters are allowed.'))


def get_image_filename(instance, old_filename):
    folder = ''
    if hasattr(instance, 'IMAGE_FOLDER'):
        folder = instance.IMAGE_FOLDER

    filename = os.path.join(
        os.path.dirname(old_filename),
        folder,
        old_filename
    )
    return filename
