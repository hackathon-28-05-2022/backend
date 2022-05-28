from django.urls import path, include

from api.views import PostList, UserMe, CommentForPostList, PostAddView, PostCreate, LikePost, DisLikePost, LikeComment, \
    DisLikeComment

urlpatterns = [
    path('posts/list/by_raiting/', PostList.as_view()),
    path('posts/create/', PostCreate.as_view()),
    path('posts/add_view/', PostAddView.as_view()),
    path('posts/like/<int:post_id>/', LikePost.as_view()),
    path('posts/dislike/<int:post_id>/', DisLikePost.as_view()),

    path('user/me/', UserMe.as_view({'get': 'list'})),
    path('comments/<int:post_id>/', CommentForPostList.as_view()),

    path('comments/like/<int:comment_id>/', LikeComment.as_view()),
    path('comments/dislike/<int:comment_id>/', DisLikeComment.as_view()),

]
