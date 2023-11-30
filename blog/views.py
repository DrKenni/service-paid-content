from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from blog.forms import ArticleForm, CommentForm
from blog.models import Article, Comment
from blog.tasks import task_delete_img


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Создание Поста"""
    model = Article
    form_class = ArticleForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

        return super().form_valid(form)


class ArticleListView(LoginRequiredMixin, ListView):
    """Список постов"""
    model = Article
    paginator_class = Paginator(Article.objects.all().order_by('-creation_date'), 12)
    template_name = 'blog/blog_list.html'
    extra_context = {
        'title': 'Статьи'
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        context_data['all_post'] = Article.objects.filter(is_published=True).order_by('-creation_date')
        return context_data


# class ArticleDetailView(LoginRequiredMixin, DetailView):
#     model = Article
#     template_name = 'blog/blog_detail.html'
#
#     def get_redirect_url(self, *args, **kwargs):
#         return redirect('blog/comment_form.html', self.kwargs.get('pk'))
#
#     def get_object(self, queryset=None):
#         self.object = super().get_object(queryset)
#         self.object.views += 1
#         self.object.save()
#         return self.object


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление поста"""
    model = Article
    form_class = ArticleForm
    template_name = 'blog/blog_form.html'
    # fields = ['title', 'content', 'image', 'video_url']

    def form_valid(self, form):
        if self.request.user == self.object.owner:
            if form.is_valid():
                form.save()
                new_mat = form.save()
                new_mat.save()

            return super().form_valid(form)
        raise Http404('Вы не являетесь владельцем поста')

    def get_success_url(self):
        return reverse('blog:comment_create', args=[self.kwargs.get('pk')])


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление поста"""
    model = Article
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if self.request.user == self.object.owner:
            if self.object.image:
                task_delete_img.delay(path=str(self.object.image))
            return super().form_valid(form)
        raise Http404('Вы не являетесь владельцем поста')


class ArticleView(ListView):
    """Главная страница"""
    model = Article
    template_name = 'blog/blog_main.html'


class CommentDeleteView(DeleteView):
    """Удаление коментария"""
    model = Comment
    success_url = reverse_lazy('blog:list')
    template_name = 'blog/comment_confirm_delete.html'

    def form_valid(self, form):
        if self.request.user == self.object.writer:
            if self.object.image:
                task_delete_img.delay(path_to=str(self.object.image))
            return super().form_valid(form)
        raise Http404('Вы не являетесь владельцем коментария')


class CommentUpdateView(UpdateView):
    """Обновление коментария"""
    model = Comment
    # success_url = reverse_lazy('blog:list')
    form_class = CommentForm

    def form_valid(self, form):
        if self.request.user == self.object.writer:
            if form.is_valid():
                new_mat = form.save()
                new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        # return reverse('blog:comment_create', args=[self.kwargs.get('pk')])
        return self.request.META.get('HTTP_REFERER')


class CommentCreateView(CreateView):
    """Создание коментария совмещенное с детальным просмотром поста"""
    model = Comment
    template_name = 'blog/comment_form.html'
    form_class = CommentForm

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        self.object = Article.objects.get(pk=self.kwargs.get('pk'))
        self.object.views += 1
        self.object.save()
        return result

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs.get('pk'))
        context_data['post'] = article
        context_data['comment_list'] = Comment.objects.filter(article=article.id)

        return context_data

    def form_valid(self, form):
        if form.is_valid():
            new_comment = form.save()
            new_comment.writer = self.request.user
            new_comment.article = Article.objects.get(pk=self.kwargs.get('pk'))
            new_comment.save()

        return super().form_valid(form)
