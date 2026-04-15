from django.urls import path
from . import api_views

urlpatterns = [
    path('notificacoes/', api_views.NotificacaoListView.as_view(), name='nsp-notificacao-list'),
    path('notificacoes/<int:pk>/', api_views.NotificacaoDetalheView.as_view(), name='nsp-notificacao-detalhe'),
    path('notificacoes/<int:pk>/analisar/', api_views.analisar_notificacao, name='nsp-analisar'),
    path('dashboard/', api_views.dashboard_nsp, name='nsp-dashboard'),
]
