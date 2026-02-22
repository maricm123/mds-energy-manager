from core.models.abstract_models import TimeStampable, DeletedAt
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class DeviceQuerySet(models.QuerySet):
    def active(self):
        return self.filter(deleted_at__isnull=True)


class DeviceManager(models.Manager.from_queryset(DeviceQuerySet)):
    pass


class ActiveDeviceManager(DeviceManager):
    def get_queryset(self):
        return super().get_queryset().active()


class Device(
    TimeStampable,
    DeletedAt
):
    name = models.CharField(max_length=100, blank=False, null=False, help_text="Device name")
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, blank=False, null=False, unique=True)
    number_of_rack_units = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    electricity_consumption = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    objects = ActiveDeviceManager()
    all_objects = DeviceManager()

    def __str__(self):
        return self.name

    def delete(self):
        self.deleted_at = timezone.now()
        # Implement delete for rack unit because of cascade and soft delete
        self.save(update_fields=["deleted_at"])
