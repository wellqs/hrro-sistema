from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.setores.models import Setor


@login_required
def registro_view(request):
    setores = Setor.objects.filter(ativo=True).order_by('nivel', 'nome')
    if not request.user.pode_ver_tudo and request.user.setor:
        setores = setores.filter(id=request.user.setor.id)
    return render(request, 'indicadores/registro.html', {
        'user': request.user,
        'setores': setores,
    })
