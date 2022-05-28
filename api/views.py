from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from api.models import Post


class PostList(generics.ListAPIView):

    def get_queryset(self):
        return Post.objects.all().order_by('-rating')
