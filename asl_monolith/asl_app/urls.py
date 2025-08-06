from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    # Serve files directly from templates directory
    urlpatterns += [
        re_path(r'^(?P<path>.*\.(js|css|png|jpg|jpeg|gif|ico))$', serve, {'document_root': settings.BASE_DIR / 'templates'}),
    ]