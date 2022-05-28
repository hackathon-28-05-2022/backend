from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView

from api.models import Post, User, Comment, Grade
from api.pagination import StandardResultsSetPagination, PageResultsSetPagination
from api.serializers import PostSerializer, UserSerializer, CommentSerializer


class PostList(generics.ListAPIView):
    pagination_class = PageResultsSetPagination
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all().order_by('-rating')


class PostCreate(generics.CreateAPIView):
    serializer_class = PostSerializer


class PostAddView(APIView):
    def post(self, request):
        data = request.POST
        post_id = data.get('post_id')
        post = Post.objects.get(id=post_id)
        post.views_count += 1
        post.save()
        return JsonResponse({'status': 'OK'})


class LikePost(APIView):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        status = Grade().like_post(user=request.user, post=post)
        if status:
            return JsonResponse({'status': 'OK'})
        else:
            return JsonResponse({'status': 'error', 'error': 'Вы уже оценили этот пост'})


class DisLikePost(APIView):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        status = Grade().dislike_post(user=request.user, post=post)
        if status:
            return JsonResponse({'status': 'OK'})
        else:
            return JsonResponse({'status': 'error', 'error': 'Вы уже оценили этот пост'})


class UserMe(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return [self.request.user]


class CommentForPostList(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_id')).order_by('rating')
