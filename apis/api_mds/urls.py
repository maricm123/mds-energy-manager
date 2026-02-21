from django.conf import settings
from django.urls import path, include
from apis.api_mds.views import (
    views_browsable
)

app_name = "api-mds"


endpoints_urlpatterns = [
]

urlpatterns = [path("", include(endpoints_urlpatterns))]

if settings.DEBUG:
    endpoints_urlpatterns_debug = [
        path("", views_browsable.APIRootView.as_view(), name="root"),
    ]
    urlpatterns += [path("", include(endpoints_urlpatterns_debug))]
