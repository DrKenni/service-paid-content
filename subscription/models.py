from django.db import models

from config import settings
from users.models import NULLABLE, SubPlan


class Subscription(models.Model):
    """Модель бесплатной подписки пользователя"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='владелец', related_name='sub')

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                verbose_name='создатель контента', related_name='creator')

    class Meta:
        verbose_name = 'бесплатная подписка'
        verbose_name_plural = 'бесплатные подписки'


class PaidSubscription(models.Model):
    """Модель платной подписки пользователя"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='владелец', related_name='paid_sub')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                verbose_name='создатель контента', related_name='paid_creator')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='дата начала подписки')
    end_time = models.DateTimeField(verbose_name='дата окончания подписки', **NULLABLE)
    active = models.BooleanField(default=False, verbose_name='активация')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'


class Payment(models.Model):
    """Модель оплаты подписки"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='пользователь', related_name='sub_own', **NULLABLE,)
    sub = models.ForeignKey(PaidSubscription, on_delete=models.CASCADE, verbose_name='Подписка',
                            related_name='sub', **NULLABLE)
    amount = models.IntegerField(verbose_name='сумма оплаты')
    date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')
    stripe_id = models.CharField(max_length=300, verbose_name='id оплаты в stripe', **NULLABLE)
    stripe_status = models.BooleanField(default=False, verbose_name='статус')
    stripe_url = models.TextField(verbose_name='url на платеж', **NULLABLE)
    redirect_url = models.URLField(verbose_name='ссылка на прошлую страницу')
    plan = models.ForeignKey(SubPlan, on_delete=models.CASCADE, verbose_name='план подписки',
                             **NULLABLE)

    def __str__(self):
        return f' {self.owner.username} подписался на {self.sub.creator.username}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
