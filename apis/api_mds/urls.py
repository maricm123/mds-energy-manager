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
        "get-all-devices",
        views_devices.GetAllDevicesView.as_view(),
        name="get-all-devices"
    ),
    path(
        "delete-device/<int:id>",
        views_devices.DeleteDeviceView.as_view(),
        name="delete-device"
    ),

    # RACKS
    path(
        "get-all-racks",
        views_rack.GetAllRacksView.as_view(),
        name="get-all-racks"
    ),
    path(
        "get-rack/<int:id>",
        views_rack.GetRackView.as_view(),
        name="get-rack"
    ),
    path(
        "create-rack",
        views_rack.CreateRackView.as_view(),
        name="create-rack"
    ),
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
