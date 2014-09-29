from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

from courses import forms
from courses import services


@login_required
def open_course(request):
    if request.method == 'GET':
        return render(request, 'courses/open.html')

    else:
        owner = request.user.profile

        form = forms.OpenCourseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            short_description = form.cleaned_data['short_description']
            course = services.open_course(
                owner, name,
                short_description=short_description
            )
            kwargs = {'course_id': course.id}
            return redirect(reverse('courses:edit', kwargs=kwargs))

        else:
            context = {'errors': []}

            errors = context['errors']
            for field in form:
                if field.errors:
                    errors.extend(field.errors)
                else:
                    context[field.name] = field.data

            return render(request, 'courses/open.html', context)


@login_required
def edit(request, course_id):
    pass
