from django.urls import path
from .views import dashboard_nir, lista_solicitacoes, nova_solicitacao, detalhe_solicitacao, painel_leitos

urlpatterns = [
    path('',                       dashboard_nir,       name='nir-dashboard-view'),
    path('painel/',                painel_leitos,       name='nir-painel'),
    path('solicitacoes/',          lista_solicitacoes,  name='nir-lista'),
    path('solicitacoes/nova/',     nova_solicitacao,    name='nir-nova'),
    path('solicitacoes/<int:pk>/', detalhe_solicitacao, name='nir-detalhe'),
]
