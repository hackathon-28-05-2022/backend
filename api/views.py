from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.models import Post, User, Comment, Grade, Advert
from api.pagination import StandardResultsSetPagination, PageResultsSetPagination
from api.serializers import PostSerializer, UserSerializer, CommentSerializer, AdvertSerializer


class PostList(generics.ListAPIView):
    """Список постов, списки сортированы по рейтингу, рейтинг скрыт"""
    pagination_class = PageResultsSetPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all().order_by('-rating')


class PostCreate(generics.CreateAPIView):
    """Создание поста"""
    serializer_class = PostSerializer


class PostAddView(APIView):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        post.views_count += 1
        post.save()
        return JsonResponse({'status': 'OK'})


class LikePost(APIView):
    """Позволяет лайкнуть пост."""

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        status = Grade().like_post(user=request.user, post=post)
        if status:
            return JsonResponse({'status': 'OK'})
        return JsonResponse({'status': 'Error', 'Error': 'Вы уже оценили этот пост'})


class DisLikePost(APIView):
    """Позволяет дизлайкнуть пост."""

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        status = Grade().dislike_post(user=request.user, post=post)
        if status:
            return JsonResponse({'status': 'OK'})
        return JsonResponse({'status': 'Error', 'Error': 'Вы уже оценили этот пост'})


class LikeComment(APIView):
    """Позволяет лайкнуть коммент."""

    def get(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        status = Grade().like_comment(user=request.user, comment=comment)
        if status:
            return JsonResponse({'status': 'OK'})
        return JsonResponse({'status': 'Error', 'Error': 'Вы уже оценили этот пост'})


class DisLikeComment(APIView):
    """Позволяет дизлайкнуть коммент."""

    def get(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        status = Grade().dislike_comment(user=request.user, comment=comment)
        if status:
            return JsonResponse({'status': 'OK'})
        return JsonResponse({'status': 'Error', 'Error': 'Вы уже оценили этот пост'})


class UserMe(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return [self.request.user]


class CommentForPostList(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_id')).order_by('rating')


class AdvertList(generics.ListAPIView):
    serializer_class = AdvertSerializer

    def get_queryset(self):
        return Advert.objects.filter(is_active=True)


class AdvertAddView(APIView):
    def get(self, request, advert_id):
        advert = Advert.objects.get(id=advert_id)
        advert.view_count += 1
        advert.save()
        return JsonResponse({'status': "OK"})


class AdvertBuy(generics.CreateAPIView):
    serializer_class = AdvertSerializer

    def create(self, request, *args, **kwargs):
        pass

