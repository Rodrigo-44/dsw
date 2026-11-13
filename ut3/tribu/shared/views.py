from django.shortcuts import render

# Create your views here.
TITLE = 'Tribu'


def index(request):
    return render(request, 'index.html', {'title': TITLE})
