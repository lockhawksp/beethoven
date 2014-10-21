from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'account/index.html')

    else:
        return redirect(reverse('quizzes:index'))
