from django.test import TestCase

from django.urls import reverse

from blog.models import Article, Comment
from blog.services import ReExpression
from subscription.models import PaidSubscription
from users.models import User


class TestReExpression(TestCase):

    def test_get_video_id(self):
        """Тест получение id видео из ссылки"""
        result = ReExpression.get_video_id(
            'https://www.youtube.com/watch?v=_1gckuhXZyw'
        )

        self.assertEquals(result, '_1gckuhXZyw')

    def test_check_url(self):
        """Тест получение bool ответ из ссылки"""
        result = ReExpression.check_url(
            'https://www.youtube.com/watch?v=_1gckuhXZyw'
        )
        self.assertEquals(result, True)

        result = ReExpression.check_url(
            'https://vk.com/feed'
        )
        self.assertEquals(result, False)


class BaseTestCase(TestCase):

    def setUp(self):
        # Саздание пользователей
        self.user1 = User.objects.create(username='test1',
                                         first_name='test1',
                                         last_name='test1',
                                         email='test1@sky.pro',
                                         is_active=True,
                                         phone=1111111111, )
        self.user1.set_password('testtest')
        self.user1.save()
        self.user2 = User.objects.create(username='test2',
                                         first_name='test2',
                                         last_name='test2',
                                         email='test2@sky.pro',
                                         is_active=True,
                                         phone=2222222222, )
        self.user2.set_password('testtest')
        self.user2.save()
        self.user3 = User.objects.create(username='test3',
                                         first_name='test3',
                                         last_name='test3',
                                         email='test3@sky.pro',
                                         is_active=True,
                                         phone=3333333333, )
        self.user3.set_password('testtest')
        self.user3.save()
        # Саздание постов пользователей
        self.post_1 = Article.objects.create(content='test1',
                                             owner=self.user1)
        self.post_2 = Article.objects.create(content='test2',
                                             owner=self.user1,
                                             is_sub=True)
        self.post_3 = Article.objects.create(content='test3',
                                             owner=self.user3,
                                             is_sub=True,
                                             is_published=False)
        # Саздание подписки пользователей
        self.sub = PaidSubscription.objects.create(owner=self.user2,
                                                   creator=self.user3)
        # Создание комментария
        self.comment_1 = Comment.objects.create(article=self.post_2,
                                                body='test1',
                                                writer=self.user2)
        self.comment_2 = Comment.objects.create(article=self.post_2,
                                                body='test2',
                                                writer=self.user3)


class TestBlog(BaseTestCase):
    """Тестирование постов"""
    def test_create_post(self):
        """Тест по созданию поста"""

        self.client.login(email=self.user1.email, password='testtest')

        data = {
            'content': 'test text',
        }

        response = self.client.post(reverse('blog:create'), data=data)
        self.assertEqual(response.status_code, 302)
        # Команда отработала и выдала редирект на другую страницу 302 код

        data_2 = {
            'content': 'test text',
            'title': 'test text',
            'video_url': 'https://vk.com/feed'
        }

        response = self.client.post(reverse('blog:create'), data=data_2)
        self.assertEqual(response.status_code, 200)
        # Отработали валидаторы по video_url. Редиректа не произошло, а значит пост не создан

        data_3 = {
            'content': 'крипта',
            'title': 'крипта',
        }

        response = self.client.post(reverse('blog:create'), data=data_3)
        self.assertEqual(response.status_code, 200)
        # Отработали валидаторы по content и title.

    def test_delete_post(self):
        """Тест на удаление поста"""

        self.client.login(email=self.user1.email, password='testtest')
        # Удаление своего поста
        response = self.client.post(f'/delete/{self.post_1.pk}/')

        self.assertEqual(response.status_code, 302)
        posts = Article.objects.count()
        self.assertEqual(posts, 2)

        # Удаление чужого поста
        response = self.client.post(f'/delete/{self.post_3.pk}/')

        self.assertEqual(response.status_code, 404)
        posts = Article.objects.count()
        self.assertEqual(posts, 2)

    def test_update_post(self):
        """Тест по обновление поста"""

        self.client.login(email=self.user1.email, password='testtest')
        data = {
            'content': 'update test',
            'title': 'update title'
        }
        # Обновление своего поста
        response = self.client.post(f'/edit/{self.post_1.pk}/', data=data)

        self.assertEqual(response.status_code, 302)
        self.post_1.refresh_from_db()
        self.assertEqual(self.post_1.title, 'update title')
        # Обновление чужого поста
        response = self.client.post(f'/edit/{self.post_3.pk}/', data=data)
        self.assertEqual(response.status_code, 404)
        self.post_3.refresh_from_db()
        self.assertEqual(self.post_3.title, None)


class TestComment(BaseTestCase):
    """Тестирование комментариев"""
    def test_create_comment(self):
        """Тест по созданию комментария"""

        self.client.login(email=self.user1.email, password='testtest')
        # Получаем список коментариев поста
        response = self.client.get(f'/comment/create/{self.post_1.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['comment_list']), 0)

        data = {
            'body': 'test text',
        }
        # Создаем коментарий и проверяем список снова
        response = self.client.post(
            reverse('blog:comment_create', kwargs={'pk': self.post_1.pk}),
            data=data
        )
        # После создания нас редиректит на эту же страницу и получаем код 302
        self.assertEqual(response.status_code, 302)

        response = self.client.get(f'/comment/create/{self.post_1.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['comment_list']), 1)

    def test_delete_comment(self):
        """Тест по удалению комментария"""
        self.client.login(email=self.user2.email, password='testtest')
        # Попытка удаления своего коментария, редирект на страницу поста
        response = self.client.post(f'/comment/delete/{self.comment_1.pk}/')

        self.assertEqual(response.status_code, 302)
        # Проверка списка коментариев
        response = self.client.get(f'/comment/create/{self.post_2.pk}/')
        self.assertEqual(len(response.context_data['comment_list']), 1)
        # Попытка удаления чужого коментария, ошибка доступа
        response = self.client.post(f'/comment/delete/{self.comment_2}/')

        self.assertEqual(response.status_code, 404)

    def test_update_comment(self):
        """Тест по обновлению комментария"""

        self.client.login(email=self.user2.email, password='testtest')
        data = {
            'body': 'update comment'
        }
        response = self.client.post(f'/comment/edit/{self.comment_1.pk}/', data=data)

        self.assertEqual(response.status_code, 302)
        self.comment_1.refresh_from_db()
        self.assertEqual(self.comment_1.body, 'update comment')
