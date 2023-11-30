from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView, TemplateView
from django.http import HttpRequest

from subscription.forms import PaidSubForm
from subscription.models import Subscription, PaidSubscription, Payment
from subscription.scr.pay import Pay
from subscription.scr.services import APIStripe
from users.models import User


class PaidSubCreateView(CreateView):
    model = PaidSubscription
    form_class = PaidSubForm

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_sub = PaidSubCreateView.objects.create(owner=self.request.user, creator=)
    #         return super().form_valid(form)


class PaidSubDeleteView(DeleteView):
    model = Subscription
    form_class = PaidSubForm


class PaymentCheckView(LoginRequiredMixin, TemplateView):
    """Проверка оплаты пользователя"""

    template_name = 'product:product_payment'

    def get(self, request, *args, **kwargs):
        """Переопределение для определения типа продукта и его
        добавления пользователю."""
        stripe_api = APIStripe()
        payment = Payment.objects.get(pk=self.kwargs.get('pk'))
        stripe_api.get_status(payment)
        if payment.stripe_status:
            payment.sub.active = True
            payment.sub.save()
        return redirect(payment.redirect_url)


class PaymentCreateView(LoginRequiredMixin, CreateView):
    """Создание платежа"""
    template_name = 'subscription:payment'

    def get(self, request, *args, **kwargs):
        """Направляет позьзователя на оплату"""
        current_site = get_current_site(request)
        previous_url = request.META.get('HTTP_REFERER')

        payment_url = Pay(user=request.user).create_payment(
            plan_pk=kwargs.get('pk'),
            previous_url=previous_url,
            domain=current_site.domain
        )
        return redirect(payment_url)


@login_required
def profile_follow(request, pk):
    """Подписка на создателя контента"""
    creator = get_object_or_404(User, pk=pk)
    if creator != request.user:
        Subscription.objects.create(
            owner=request.user,
            creator=creator,
        )
    return redirect(
        'users:profile',
        creator.pk
    )


@login_required
def profile_unfollow(request, pk):
    """Отписка от создателя контента"""
    creator = get_object_or_404(User, pk=pk)
    Subscription.objects.filter(
        owner=request.user,
        creator=creator,
    ).delete()
    return redirect(
        'users:profile',
        creator.pk
    )
