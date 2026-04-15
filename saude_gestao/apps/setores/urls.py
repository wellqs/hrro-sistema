from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.SetorListView.as_view(), name='setor-list'),
    path('organograma/', api_views.organograma_view, name='organograma'),
    path('resumo/', api_views.resumo_setores, name='resumo-setores'),
    path('<str:codigo>/', api_views.SetorDetalheView.as_view(), name='setor-detalhe'),
]
