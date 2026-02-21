from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampable(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("creations"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("last modification"))
