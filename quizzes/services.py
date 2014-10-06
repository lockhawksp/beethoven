from quizzes.models import Article, Quiz, AnswerSheet, Answer


def create_quiz(course):
    quiz = Quiz()
    quiz.course = course
    quiz.save()
    return quiz


def create_article(quiz, title, content, source_url=None):
    article = Article(title=title, content=content)
    article.source_url = source_url
    article.save()

    quiz.article = article
    quiz.save()


def update_questions(quiz, new_questions):
    new_questions_set = set(new_questions)
    seq_dict = {
        q: (i+1) for (i, q) in enumerate(new_questions)
    }

    current_question_objects = quiz.questions.all()
    current_question_strings_set = set(
        q.question for q in current_question_objects
    )

    unchanged_question_strings = current_question_strings_set.intersection(
        new_questions_set
    )
    added_question_strings = new_questions_set - unchanged_question_strings
    deleted_questions = (current_question_strings_set -
                         unchanged_question_strings)

    for question in current_question_objects:
        if question.question in deleted_questions:
            question.delete()

        if question.question in unchanged_question_strings:
            question.sequence = seq_dict[question.question]
            question.save()

    for question in added_question_strings:
        quiz.questions.create(
            question=question,
            sequence=seq_dict[question]
        )


def create_answer_sheet(assigned_to, quiz):
    answer_sheet = AnswerSheet(quiz=quiz, assigned_to=assigned_to)
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
