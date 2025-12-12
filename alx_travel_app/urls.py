"""
URL configuration for alx_travel_app project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("alx_travel_app.urls")),
]

# Include swagger URLs separately
# try:
#     from .swagger_urls import urlpatterns as swagger_urls
#     urlpatterns += swagger_urls
# except Exception as e:
#     print(f"Swagger not loaded: {e}")
