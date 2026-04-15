from django.urls import path
from .views import dashboard_nsp, lista_notificacoes, nova_notificacao, detalhe_notificacao, metas_seguranca

urlpatterns = [
    path('', dashboard_nsp, name='nsp-dashboard-view'),
    path('notificacoes/', lista_notificacoes, name='nsp-lista'),
    path('notificacoes/nova/', nova_notificacao, name='nsp-nova'),
    path('notificacoes/<int:pk>/', detalhe_notificacao, name='nsp-detalhe'),
    path('metas/', metas_seguranca, name='nsp-metas'),
]
