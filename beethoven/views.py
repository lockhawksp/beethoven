from django.shortcuts import render


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'beethoven/index.html')
