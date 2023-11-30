from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from config import settings

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователя"""

    username = models.CharField(max_length=150, verbose_name='псевдоним', unique=True)
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    surname = models.CharField(max_length=150, verbose_name='отчество', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')

    about_me = models.CharField(max_length=300, verbose_name='о себе', **NULLABLE)
    description = models.CharField(max_length=400, verbose_name='комментарий', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=10, verbose_name='телефон', unique=True, **NULLABLE)
    sex = models.CharField(choices=(('male', 'Мужской пол'), ('female', 'Женский пол')),
                           default="male", max_length=40)

    is_staff = models.BooleanField(default=False, verbose_name='персонал')
    is_active = models.BooleanField(default=False, verbose_name='активность')
    is_superuser = models.BooleanField(default=False, verbose_name='супер пользователь')
    hidden_prof = models.BooleanField(default=False, verbose_name='профиль скрыт')

    creation_date = models.DateTimeField(auto_now_add=timezone.now,
                                         verbose_name='дата создания аккаунта')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class SubPlan(models.Model):
    """Модель плана подписки на пользователя"""

    CHOICES_PLAN = [
        (1, 'месяц'),
        (3, 'три месяца'),
        (6, 'шесть месяцев'),
        (12, 'двенадцать месяцев')
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='владелец',
                              related_name='plan_own', on_delete=models.CASCADE,
                              **NULLABLE)

    name = models.CharField(max_length=150, verbose_name='название')
    price = models.PositiveIntegerField(default=1, verbose_name='стоймость')
    length = models.PositiveIntegerField(choices=CHOICES_PLAN, default=1, verbose_name='длительность')
    stripe_product_id = models.CharField(max_length=150, verbose_name='ID Stripe продукт', **NULLABLE)
    stripe_price_id = models.CharField(max_length=150, verbose_name='ID Stripe цена', **NULLABLE)


class Verify(models.Model):
    """Модель верификации по номеру телефона"""
    user = models.OneToOneField(User, verbose_name='пользователь', on_delete=models.CASCADE,
                                related_name='verify')
    code = models.PositiveIntegerField(verbose_name='код верификации')
    user_input = models.PositiveIntegerField(verbose_name='код пользователя', **NULLABLE)
