from django.urls import path, include

from api.views import PostList, UserMe

urlpatterns = [
    path('posts/list/by_raiting/', PostList.as_view()),
    path('user/me/', UserMe.as_view({'get': 'list'}))

]
