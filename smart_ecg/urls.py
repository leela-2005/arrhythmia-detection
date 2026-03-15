from django.contrib import admin
from django.urls import path, include
from ecg.views import upload_ecg
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/', include('modern_auth.urls')), # New module
    path('accounts/', include('allauth.urls')), # Google OAuth
    path('', include('dashboard.urls')),
    path('upload/', upload_ecg, name='upload'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)