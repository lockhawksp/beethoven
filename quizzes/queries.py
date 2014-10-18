from quizzes.models import Quiz, AnswerSheet


def find_submitted_answer_sheets(profile):
    return AnswerSheet.objects.filter(owner=profile, submitted=True)


def find_done_quiz_ids(profile):
    q = find_submitted_answer_sheets(profile)
    return q.values_list('quiz__id', flat=True)


def find_new_assignments(profile):
    q = Quiz.objects.filter(assigned_to=profile)
    return q.exclude(id__in=find_done_quiz_ids(profile))


def new_assignment_number(profile):
    q = find_new_assignments(profile)
    return q.count()


def find_done_assignments(profile):
    q = Quiz.objects.filter(assigned_to=profile)
    return q.filter(id__in=find_done_quiz_ids(profile))
