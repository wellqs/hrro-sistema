from django.urls import path
from .views import dashboard, setor_detalhe, organograma, alertas_view, registro_view

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('setor/<str:codigo>/', setor_detalhe, name='setor-detalhe'),
    path('organograma/', organograma, name='organograma'),
    path('alertas/', alertas_view, name='alertas'),
    path('registro/', registro_view, name='registro'),
]
