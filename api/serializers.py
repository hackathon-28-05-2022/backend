from rest_framework import serializers

from api.models import Post, User, Grade, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'author',
            'created_at',
            'id',
            'likes_count',
            'dislikes_count',
        ]

    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    def get_likes_count(self, post):
        return Grade.objects.filter(is_like=True, post=post).count()

    def get_dislikes_count(self, post):
        return Grade.objects.filter(is_dislike=True, post=post).count()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['electricity', 'username', 'coin_balance', 'date_joined', 'pulse']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body', 'author', 'created_at', 'dislikes_count', 'likes_count', 'id']

    dislikes_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, comment):
        return Grade.objects.filter(is_like=True, comment=comment).count()

    def get_dislikes_count(self, comment):
        return Grade.objects.filter(is_dislike=True, comment=comment).count()
