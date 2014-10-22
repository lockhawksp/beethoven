from django.utils.timezone import now

from guardian.shortcuts import assign_perm

from quizzes.models import Article, Quiz, AnswerSheet, Answer, Question


def create_quiz(owner, course, assigned_to=None, deadline=None):
    quiz = Quiz(owner=owner, course=course)
    quiz.save()

    # Assign permissions for owner of quiz
    assign_perm('edit_quiz', owner.user, quiz)
    assign_perm('delete_quiz', owner.user, quiz)

    if assigned_to is None:
        assigned_to = course.students.all()

    quiz.assigned_to.add(*assigned_to)
    for p in assigned_to:
        assign_perm('attempt_quiz', p.user, quiz)

    if deadline:
        quiz.due = deadline
        quiz.save()

    return quiz


def create_article(quiz, title, content, source_url=None):
    article = Article(title=title, content=content)
    article.source_url = source_url
    article.save()

    quiz.article = article
    quiz.save()


def update_questions(quiz, new_questions):
    quiz.questions.all().delete()

    for i, question in enumerate(new_questions):
        if question != '':
            quiz.questions.create(
                question=question,
                sequence=i+1
            )


def create_answer_sheet(owner, quiz):
    answer_sheet = AnswerSheet(quiz=quiz, owner=owner)
    answer_sheet.save()

    questions = quiz.questions.all()

    for question in questions:
        answer_sheet.answers.create(question=question)

    return answer_sheet


def update_answers(new_answers):
    for a in new_answers:
        answer_id = a['id']
        answer_str = a['answer']

        current_answer = Answer.objects.get(pk=answer_id)
        current_answer.answer = answer_str
        current_answer.save()


def is_due(quiz):
    if quiz.due is None:
        return False
    else:
        return quiz.due < now()


def update_solutions(new_solutions):
    for solution in new_solutions:
        question_id = solution['question_id']
        solution_str = solution['solution']

        question = Question.objects.get(pk=question_id)
        question.standard_answer = solution_str
        question.save()
