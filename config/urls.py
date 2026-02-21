from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # API URL
    path("api-mds/", include("apis.api_mds.urls", namespace="api-mds")),
]
