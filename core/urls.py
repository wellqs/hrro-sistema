from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda r: redirect('dashboard'), name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.setores.urls_views')),
    path('api/auth/', include('apps.accounts.api_urls')),
    path('api/setores/', include('apps.setores.urls')),
    path('api/indicadores/', include('apps.indicadores.urls')),
    path('api/alertas/', include('apps.alertas.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
