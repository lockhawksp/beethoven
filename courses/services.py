from courses.models import Course


def open_course(owner, name, short_description=None):
    course = Course()
    course.owner = owner
    course.name = name
    if short_description is not None:
        course.short_description = short_description
    course.save()
    return course
