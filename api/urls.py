from django.urls import path, include

from api.views import PostList

urlpatterns = [
    path('posts/list/by_raiting/', PostList.as_view()),

]
