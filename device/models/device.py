from core.models.abstract_models import TimeStampable, DeletedAt
from django.db import models
from django.core.validators import MinValueValidator
from rack.models import Rack
from django.utils import timezone


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            deleted_at__isnull=True
        )


class Device(
    TimeStampable,
    DeletedAt
):
    name = models.CharField(max_length=100, blank=False, null=False, help_text="Device name")
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, blank=False, null=False, unique=True)
    number_of_rack_units = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    electricity_consumption = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    objects = ActiveManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.name

    def delete(self):
        self.deleted_at = timezone.now()
        # Implement delete for rack unit because of cascade and soft delete
        self.save(update_fields=["deleted_at"])
