from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView

from api.models import Post, User
from api.serializers import PostSerializer, UserSerializer


class PostList(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all().order_by('-rating')


class UserMe(APIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user
