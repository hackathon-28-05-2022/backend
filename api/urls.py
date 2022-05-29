from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from api.views import PostList, UserMe, CommentForPostList, PostAddView, PostCreate, LikePost, DisLikePost, LikeComment, \
    DisLikeComment, AdvertList

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('posts/list/by_raiting/', PostList.as_view()),
    path('posts/create/', PostCreate.as_view()),
    path('posts/add_view/', PostAddView.as_view()),
    path('posts/like/<int:post_id>/', LikePost.as_view()),
    path('posts/dislike/<int:post_id>/', DisLikePost.as_view()),

    path('user/me/', UserMe.as_view({'get': 'list'})),
    path('comments/<int:post_id>/', CommentForPostList.as_view()),

    path('comments/like/<int:comment_id>/', LikeComment.as_view()),
    path('comments/dislike/<int:comment_id>/', DisLikeComment.as_view()),

    path('advert/list/', AdvertList.as_view()),
    path('docs/', include_docs_urls(title='ABOBA Inn'))
]
