from django.conf import settings
from django.db import models
from django.utils import timezone

from users.models import NULLABLE
from users.services import user_directory_path


class Article(models.Model):
    """Модель статей пользователя"""

    title = models.CharField(max_length=150, verbose_name='заголовок', **NULLABLE)
    content = models.TextField(verbose_name='содержимое')
    image = models.ImageField(upload_to=user_directory_path, verbose_name='превью', **NULLABLE)
    creation_date = models.DateField(auto_now_add=timezone.now, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='признак публичности')
    is_sub = models.BooleanField(default=False, verbose_name='доступ по подписке')
    views = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              verbose_name='владелец', **NULLABLE)
    video_url = models.URLField(verbose_name='ссылка на видео', **NULLABLE)

    def __str__(self):
        return f'{self.owner} написал {self.creation_date}'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'


class Comment(models.Model):
    """Модель комментариев"""

    body = models.TextField(verbose_name='содержимое')
    article = models.ForeignKey(Article, verbose_name='статья', on_delete=models.CASCADE,
                                related_name='comment')
    image = models.ImageField(upload_to=user_directory_path, verbose_name='превью', **NULLABLE)
    active = models.BooleanField(default=True)
    creation_date = models.DateField(auto_now_add=timezone.now, verbose_name='дата создания')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                               verbose_name='владелец', **NULLABLE)

    class Meta:
        verbose_name = 'коментарий'
        verbose_name_plural = 'коментарии'
