from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def alertas_view(request):
    return render(request, 'alertas/alertas.html', {'user': request.user})
