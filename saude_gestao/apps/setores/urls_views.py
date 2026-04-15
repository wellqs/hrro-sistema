from django.urls import path
from .views import dashboard, setor_detalhe, organograma

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('setor/<str:codigo>/', setor_detalhe, name='setor-detalhe'),
    path('organograma/', organograma, name='organograma'),
]
