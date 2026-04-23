from django.urls import path
from .views import dashboard_gfisio, lista_atendimentos, novo_atendimento, detalhe_atendimento

urlpatterns = [
    path('', dashboard_gfisio, name='gfisio-dashboard-view'),
    path('atendimentos/', lista_atendimentos, name='gfisio-lista'),
    path('atendimentos/novo/', novo_atendimento, name='gfisio-novo'),
    path('atendimentos/<int:pk>/', detalhe_atendimento, name='gfisio-detalhe-view'),
]
