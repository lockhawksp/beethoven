from rest_framework import serializers

from quizzes.models import Article


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
