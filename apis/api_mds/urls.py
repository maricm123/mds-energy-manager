from django.conf import settings
from django.urls import path, include
from apis.api_mds.views import (
    views_browsable,
    views_rack,
    views_devices
)

app_name = "api-mds"


endpoints_urlpatterns = [
    # DEVICES
    path(
        "delete-device/<int:id>",
        views_devices.DeleteDeviceView.as_view(),
        name="delete-device"
    ),

    # RACKS
    path(
        "delete-rack/<int:id>",
        views_rack.DeleteRackView.as_view(),
        name="delete-rack"
    )
]

urlpatterns = [path("", include(endpoints_urlpatterns))]

if settings.DEBUG:
    endpoints_urlpatterns_debug = [
        path("", views_browsable.APIRootView.as_view(), name="root"),
    ]
    urlpatterns += [path("", include(endpoints_urlpatterns_debug))]
