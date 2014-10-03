from quizzes.models import Article, MetaQuiz


def create_meta_quiz(course):
    meta_quiz = MetaQuiz()
    meta_quiz.course = course
    meta_quiz.save()
    return meta_quiz


def create_article(quiz, title, content, source_url=None):
    article = Article(title=title, content=content)
    article.source_url = source_url
    article.save()

    quiz.article = article
    quiz.save()
