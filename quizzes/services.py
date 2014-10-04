from quizzes.models import Article, Quiz


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
