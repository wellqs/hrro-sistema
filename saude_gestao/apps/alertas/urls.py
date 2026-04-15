from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.AlertaListView.as_view(), name='alerta-list'),
    path('contagem/', api_views.contagem_alertas, name='alerta-contagem'),
    path('marcar-todos-lidos/', api_views.marcar_todos_lidos, name='marcar-todos-lidos'),
    path('<int:pk>/lido/', api_views.marcar_lido, name='alerta-lido'),
]
