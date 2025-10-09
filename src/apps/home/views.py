from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .context import usercontext


@login_required
def index(request):
    context = usercontext(request)
    context.update(
        {
            "titre_onglet": "Démo",
            "titre_presentation": "Démonstration",
        }
    )
    return render(request, "home/index.html", context)
