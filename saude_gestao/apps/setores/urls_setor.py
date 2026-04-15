from django.urls import path
from .views import setor_hub

urlpatterns = [
    path('', setor_hub, name='setor-hub'),
]
