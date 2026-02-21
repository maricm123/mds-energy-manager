from core.models.abstract_models import TimeStampable
from django.db import models
from django.core.validators import MinValueValidator


class Rack(
    TimeStampable
):
    name = models.CharField(max_length=100, blank=False, null=False, help_text="Rack name")
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, blank=False, null=False, unique=True)
    total_units = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    max_electricity_sustained = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name
