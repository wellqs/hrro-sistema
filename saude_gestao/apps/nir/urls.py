from django.urls import path
from . import api_views

urlpatterns = [
    path('solicitacoes/',                  api_views.SolicitacaoListView.as_view(),    name='nir-solicitacao-list'),
    path('solicitacoes/<int:pk>/',         api_views.SolicitacaoDetalheView.as_view(), name='nir-solicitacao-detalhe'),
    path('solicitacoes/<int:pk>/regular/', api_views.regular_solicitacao,              name='nir-regular'),
    path('dashboard/',                     api_views.dashboard_nir,                    name='nir-dashboard'),
    path('painel/',                        api_views.painel_leitos,                    name='nir-painel-api'),
    path('leitos/<int:pk>/status/',        api_views.atualizar_leito,                  name='nir-leito-status'),
]
