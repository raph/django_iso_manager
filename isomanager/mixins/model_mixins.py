from django.db import models
from django.utils.translation import gettext as _


class TimeMixin(models.Model):
    created_time = models.DateTimeField(_("Created Time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("Updated Time"), auto_now=True)

    class Meta:
        abstract = True
