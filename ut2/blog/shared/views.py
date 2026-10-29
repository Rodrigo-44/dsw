from django.shortcuts import render


# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')


def custom_404(request, exception):
    context = {}
    return render(request, '404.html', context, status=404)
