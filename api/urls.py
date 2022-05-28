from django.urls import path, include

from api.views import PostList

urlpatterns = [
    path('posts/list/', PostList.as_view())
]
