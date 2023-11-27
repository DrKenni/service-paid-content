from django.contrib import admin

from blog.models import Article, Comment


@admin.register(Article)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('content', 'creation_date', 'is_published', 'owner')
    list_filter = ('content', 'creation_date', 'is_published', 'owner')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'article', 'active', 'writer')
    list_filter = ('body', 'article', 'active', 'writer')