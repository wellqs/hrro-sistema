from django.urls import path
from . import api_views

urlpatterns = [
    path('atendimentos/', api_views.AtendimentoListView.as_view(), name='gfisio-list'),
    path('atendimentos/<int:pk>/', api_views.AtendimentoDetalheView.as_view(), name='gfisio-detalhe'),
    path('atendimentos/<int:pk>/evolucao/', api_views.registrar_evolucao, name='gfisio-evolucao'),
    path('dashboard/', api_views.dashboard_gfisio, name='gfisio-dashboard'),
]
