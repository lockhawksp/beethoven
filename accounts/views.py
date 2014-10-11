from django.shortcuts import render


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'account/index.html')

    else:
        return render(request, 'account/user_home.html')
