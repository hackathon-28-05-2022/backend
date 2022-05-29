from django.contrib import admin

# Register your models here.
from api.models import User, Post, Comment, Grade, Advert


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author',)


@admin.register(Grade)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ('id',)
