from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.IndicadorListView.as_view(), name='indicador-list'),
    path('registros/', api_views.RegistroListView.as_view(), name='registro-list'),
    path('registros/<int:pk>/', api_views.RegistroDetalheView.as_view(), name='registro-detalhe'),
    path('grafico/<str:codigo>/', api_views.grafico_setor, name='grafico-setor'),
    path('dashboard/', api_views.dashboard_consolidado, name='dashboard-consolidado'),
]
