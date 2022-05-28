from django.urls import path, include

from api.views import PostList, UserMe, CommentForPostList, PostAddView

urlpatterns = [
    path('posts/list/by_raiting/', PostList.as_view()),
    path('posts/add_view/', PostAddView.as_view()),
    path('user/me/', UserMe.as_view({'get': 'list'})),
    path('comments/<int:post_id>/', CommentForPostList.as_view())

]
