from rest_framework import serializers

from quizzes.models import Article, Quiz, Question, Answer, AnswerSheet


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
            'id',
            'question',
            'sequence',
        )


class AnswerSerializer(serializers.ModelSerializer):

    question = serializers.PrimaryKeyRelatedField()

    class Meta(object):
        model = Answer
        fields = (
            'id',
            'question',
            'answer',
            'created_at',
            'updated_at'
        )


class AnswerSheetSerializer(serializers.ModelSerializer):

    answers = AnswerSerializer(many=True)

    class Meta(object):
        model = AnswerSheet
        fields = (
            'id',
            'answers',
            'created_at',
            'updated_at',
            'scored'
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
            'due'
        )
