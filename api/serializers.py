from rest_framework import serializers

from api.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body', 'author', 'created_at', 'rating', 'id']

