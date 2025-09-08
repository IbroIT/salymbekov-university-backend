# back_su_m/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('news.urls')),  # News API endpoints
    path('research/', include('research.urls')),  # Research API endpoints
    path('api/careers/', include('careers.urls')),  # Careers API endpoints
    path('api/banners/', include('banner.urls')),  # Banner API endpoints - ВО МНОЖЕСТВЕННОМ ЧИСЛЕ!
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)