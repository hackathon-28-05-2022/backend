from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from api.views import PostList, UserMe, CommentForPostList, PostAddView, PostCreate, LikePost, DisLikePost, LikeComment, \
    DisLikeComment

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import ListLots, BuyLot

urlpatterns = [
    path('list/', ListLots.as_view()),
    path('buy/', BuyLot.as_view()),
]
