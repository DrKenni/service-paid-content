import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from blog.models import Article
from subscription.models import Subscription, PaidSubscription

from users.forms import UserRegisterForm, UserProfileForm, UserViewForm, SubPlanView, CustomAuthenticationForm, \
    VerifyForm
from users.models import User, SubPlan, Verify
from users.services import send_code


class UserDetailView(DetailView):
    """Просмотр профиля пользователя"""
    model = User
    form_clss = UserViewForm
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Получение пользователя
        user = User.objects.get(pk=self.kwargs.get('pk'))
        context_data['user'] = user

        # Посты пользователя
        context_data['post_list'] = Article.objects.filter(owner=user).order_by('-creation_date')
        context_data['best_post'] = Article.objects.filter(owner=user,
                                                           is_sub=False).order_by('-views').first
        context_data['discussed_post'] = Article.objects.filter(owner=user).order_by('-comment').first
        # подписки на пользователя
        try:
            context_data['i_sub'] = Subscription.objects.get(owner=self.request.user,
                                                             creator=user)
        except ObjectDoesNotExist:
            context_data['i_sub'] = None
        try:
            context_data['i_paid_sub'] = PaidSubscription.objects.get(owner=self.request.user,
                                                                      creator=user)
        except ObjectDoesNotExist:
            context_data['i_paid_sub'] = None
        try:
            context_data['plan'] = bool(SubPlan.objects.filter(owner=user))
        except ObjectDoesNotExist:
            context_data['plan'] = False
        try:
            context_data['sub_list'] = PaidSubscription.objects.filter(creator=user)
        except ObjectDoesNotExist:
            context_data['sub_list'] = False

        return context_data


class RegisterView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # with transaction.atomic():
        self.object = form.save()

        code = random.randint(0000, 9999)
        verify = Verify.objects.create(user=self.object, code=code)

        send_code(numb=self.object.phone,
                  code=verify.code)

        return redirect(reverse('users:verify', kwargs={'pk': verify.pk}))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('blog:main')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['plan_list'] = SubPlan.objects.filter(owner=self.object.pk)
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            form.save()

            return super().form_valid(form)


class UserView(ListView):
    model = User
    form_class = UserViewForm
    template_name = 'user/user_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['user_list'] = User.objects.exclude(is_superuser=True, pk=self.request.user.pk)
        return context_data


class SubPlanListView(ListView):
    model = SubPlan
    form_class = SubPlanView
    template_name = 'users/plan_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs.get('pk'))
        context_data['user'] = user
        context_data['plan_list'] = SubPlan.objects.filter(owner=user)
        return context_data


class SubPlanCreateView(CreateView):
    model = SubPlan
    form_class = SubPlanView
    template_name = 'users/plan_form.html'
    success_url = reverse_lazy('blog:main')

    def form_valid(self, form):
        if form.is_valid():
            new_plan = form.save()
            new_plan.save()

            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()

        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True


class VerifyView(UpdateView):
    model = Verify
    form_class = VerifyForm

    def form_valid(self, form):
        self.object = form.save()
        user = self.object.user
        user.is_active = True
        user.save()
        self.object.delete()
        return redirect(reverse('users:login'))


class VerifyAgain(UpdateView):
    model = Verify

    def get(self, request, *args, **kwargs):
        verify = Verify.objects.get(pk=self.kwargs.get('pk'))
        code = random.randint(0000, 9999)
        verify.code = code
        verify.save()

        send_code(numb=verify.user.phone, code=code)
        return redirect(reverse('users:verify', kwargs={'pk': verify.pk}))
