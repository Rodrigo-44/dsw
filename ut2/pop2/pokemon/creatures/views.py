from django.http import HttpResponse
from django.shortcuts import render

from .models import Creature

# Create your views here.


def creature_list(request):
    total_creatures = Creature.objects.count()
    creatures = Creature.objects.order_by('-name')
    return render(
        request,
        'creatures/creature/list.html',
        {
            'title': 'Pokemon',
            'subtitle': 'Creature detail',
            'creatures': creatures,
            'total_creatures': total_creatures,
        },
    )


def creture_detail(request, post_slug: str):
    try:
        creature = Creature.objects.get(slug=post_slug)
    except Creature.DoesNotExist:
        return HttpResponse(f'Post with slug "{post_slug}" does not exist!')
    return render(
        request,
        'creatures/creature/detail.html',
        {
            'title': 'Pokemon',
            'subtitle': 'Creature detai',
            'creature': creature,
        },
    )
