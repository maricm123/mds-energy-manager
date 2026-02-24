from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # API URL
    path("api-mds/", include("apis.api_mds.urls", namespace="api-mds")),
    path("api-mds/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api-mds/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api-mds/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
