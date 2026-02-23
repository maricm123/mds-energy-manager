from core.models.abstract_models import TimeStampable, DeletedAt
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class RackQuerySet(models.QuerySet):
    def active(self):
        return self.filter(deleted_at__isnull=True)


class RackManager(models.Manager.from_queryset(RackQuerySet)):
    pass


class ActiveRackManager(RackManager):
    def get_queryset(self):
        return super().get_queryset().active()


class Rack(
    TimeStampable,
    DeletedAt
):
    name = models.CharField(max_length=100, blank=False, null=False, help_text="Rack name")
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, blank=False, null=False, unique=True)
    total_units = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    max_electricity_sustained = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    objects = ActiveRackManager()
    all_objects = RackManager()

    def __str__(self):
        return self.name
