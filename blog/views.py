
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from blog.forms import ArticleForm
from blog.models import Article, Comment
from blog.tasks import task_delete_img


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:list')
    # extra_context = {'previous_page': HttpRequest.META.get['HTTP_REFERER']}

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.save()
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

        return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     redirect_url = request.META.get('HTTP_REFERER')
    #     return redirect_url


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    paginator_class = Paginator(Article.objects.all().order_by('-creation_date'), 12)
    template_name = 'blog/blog_list.html'
    extra_context = {
        'title': 'Статьи'
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        context_data['all_post'] = Article.objects.all().order_by('-creation_date')
        return context_data


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    # success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление поста"""
    model = Article
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            if self.object.image:
                task_delete_img.delay(path_to=str(self.object.image))

        return super().form_valid(form)


class ArticleView(ListView):
    model = Article
    template_name = 'blog/blog_main.html'


class CommentDeleteView(DeleteView):
    model = Comment
    success_url = reverse_lazy('blog:list')


class CommentUpdateView(UpdateView):
    model = Comment
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])
