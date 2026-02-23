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
        "create-device",
        views_devices.CreateDeviceView.as_view(),
        name="create-device"
    ),
    path(
        "add-device-to-rack",
        views_devices.AddDeviceToRackView.as_view(),
        name="add-device-to-rack"
    ),
    path(
        "update-device/<int:id>",
        views_devices.UpdateDeviceView.as_view(),
        name="update-device"
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
        "update-rack/<int:id>",
        views_rack.UpdateRackView.as_view(),
        name="update-rack"
    ),
    path(
        "delete-rack/<int:id>",
        views_rack.DeleteRackView.as_view(),
        name="delete-rack"
    ),
    path(
        "suggest-algorithm",
        views_rack.DeviceUnitsSuggestionView.as_view(),
        name="suggest-algorithm"
    )
]

urlpatterns = [path("", include(endpoints_urlpatterns))]

if settings.DEBUG:
    endpoints_urlpatterns_debug = [
        path("", views_browsable.APIRootView.as_view(), name="root"),
    ]
    urlpatterns += [path("", include(endpoints_urlpatterns_debug))]
