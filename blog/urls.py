from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleCreateView, ArticleListView, ArticleUpdateView, ArticleDeleteView, \
    ArticleView, CommentDeleteView, CommentUpdateView, CommentCreateView

app_name = BlogConfig.name

urlpatterns = [
    path('', ArticleView.as_view(), name='main'),
    # Blog
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('list/', ArticleListView.as_view(), name='list'),
    # path('view/<int:pk>/', ArticleDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', ArticleUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ArticleDeleteView.as_view(), name='delete'),
    # Comment
    path('comment/edit/<int:pk>/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/create/<int:pk>/', CommentCreateView.as_view(), name='comment_create'),
]
