from rest_framework import serializers

from api.models import Post, User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body', 'author', 'created_at', 'rating', 'id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['electricity', 'username', 'coin_balance']
