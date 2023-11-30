from blog.tests import BaseTestCase


# class TestSubscription(BaseTestCase):
#     """Тестирование подписок"""
#     def test_create_subscription(self):
#         """Тест по подписке пользователя"""
#         self.client.login(email=self.user1.email, password='testtest')
#
#         response = self.client.post(f'/subscribe/{self.user2.pk}/')
#         self.assertEqual(response.status_code, 302)

class TestPaidSubscription(BaseTestCase):
    """Тестрирование платной подписки"""
    def test_paid_subscription(self):
        pass

    def test_get_paid_content(self):
        """Тест на доступ к контенту с доступом по платной подписке"""
        # проверка с подписаным пользователем
        self.client.login(email=self.user2.email, password='testtest')
        response = self.client.get(f'/users/profile/{self.user3.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['post_list']), 1)
        self.client.logout()
        # проверка с неподписаным пользователем(пока не реализовано)
        # self.client.login(email=self.user1.email, password='testtest')
        # response = self.client.get(f'/users/profile/{self.user3.pk}/')
        # print(response.context_data['post_list'])
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.context_data['post_list']), 0)
