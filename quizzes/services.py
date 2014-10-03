from quizzes.models import MetaQuiz


def create_meta_quiz(course):
    meta_quiz = MetaQuiz()
    meta_quiz.course = course
    meta_quiz.save()
    return meta_quiz
