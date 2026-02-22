from django.contrib import admin
from .models.rack import Rack
from .models.rack_units import RackUnit


admin.site.register(Rack)
admin.site.register(RackUnit)
