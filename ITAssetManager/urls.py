from django.contrib import admin
from django.urls import path, include
from .views import home, load_db_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("assets/", include("itassets.urls")), #connects it assets
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)