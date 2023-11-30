import os

from celery import shared_task
from django.utils import timezone

from config import settings
from subscription.models import PaidSubscription


@shared_task
def check_sub():
    """Каждый час проверяет на срок действия подписки,
    если подписка истекает, то удаляет объукт подписки"""

    sub_list = PaidSubscription.objects.all()
    for sub in sub_list:
        if sub.end_time <= timezone.now():
            sub.delete()


@shared_task
def task_delete_img(path):
    """Удаление файла по указанному пути"""
    os.remove(os.path.join(settings.MEDIA_ROOT, path))

