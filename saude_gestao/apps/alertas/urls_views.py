from django.urls import path
from .views import alertas_view

urlpatterns = [
    path('alertas/', alertas_view, name='alertas'),
]
