from rest_framework import serializers

from quizzes.models import Article, Quiz, Question


class ArticleSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Article
        fields = (
            'title',
            'content',
            'source_url',
            'created_at',
            'updated_at'
        )

    def transform_source_url(self, obj, value):
        if value is None:
            value = ''
        return value


class QuestionSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Question
        fields = (
            'question',
            'sequence',
        )


class QuizSerializer(serializers.ModelSerializer):
    article = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='quizzes_api:article_details'
    )
    questions = QuestionSerializer()

    class Meta(object):
        model = Quiz
        fields = (
            'article',
            'questions',
            'created_at',
            'updated_at',
            'due',
            'attempted',
            'last_attempt'
        )
