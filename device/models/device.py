from core.models.abstract_models import TimeStampable, DeletedAt
from django.db import models
from django.core.validators import MinValueValidator
from rack.models import Rack
from django.utils import timezone


class Device(
    TimeStampable,
    DeletedAt
):
    name = models.CharField(max_length=100, blank=False, null=False, help_text="Device name")
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, blank=False, null=False, unique=True)
    number_of_rack_units = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    electricity_consumption = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    rack = models.ForeignKey(
        Rack,
        related_name="devices",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])
