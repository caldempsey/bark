import datetime
import os
import random
import string

from django.db import models


def upload_to(instance, filename):
    """
    Function used to create a secure string. Ensures uniqueness of file upload names.
    https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.FileField.upload_to
    """
    datetime_string = datetime.datetime.now().strftime("%d%m%Y")
    hash = create_secure_string()
    filename_base, filename_ext = os.path.splitext(filename)
    while os.path.isdir(datetime_string + hash + "/"):
        hash = create_secure_string()
    filepath_out = datetime_string + hash + "/" + datetime_string + hash + filename_ext.lower()
    return filepath_out


def create_secure_string():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10))


class Resources(models.Model):
    file = models.FileField(upload_to=upload_to, blank=False, max_length=500)

    class Meta:
        verbose_name_plural = "Resources"
