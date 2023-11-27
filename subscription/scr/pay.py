from datetime import timedelta
from typing import Any

from subscription.models import Payment, PaidSubscription
from subscription.scr.services import APIStripe
from users.models import SubPlan


class Pay:
    """Класс для работы с платежами"""

    def __init__(self, user: Any = None):
        self.stripe = APIStripe()
        self.user = user
        self.payment = None
        self.status = None

    def create_payment(self, plan_pk,
                       previous_url: str,
                       domain: str) -> str:
        """Метод создает модели платежа и подписки,
        возвращает ссылку на оплату"""

        plan = SubPlan.objects.get(pk=plan_pk)
        sub = PaidSubscription.objects.create(owner=self.user,
                                              creator=plan.owner)
        sub.end_time = sub.start_time + timedelta(days=plan.length * 30)
        sub.save()
        self.payment = Payment.objects.create(owner=self.user,
                                              sub=sub,
                                              plan=plan,
                                              amount=plan.price,
                                              redirect_url=previous_url)
        self.payment.save()
        check_url = f'http://{domain}/subscribe/payment/check/{self.payment.pk}/'

        response = self.stripe.get_payment_link(check_url, plan.stripe_price_id)
        self.payment.stripe_id = response['id']
        self.payment.stripe_url = response['url']
        self.payment.save()

        return response['url']

    def check_payment(self):
        """Метод проверяет статус платежа и обновляет его в БД"""

        status = self.stripe.get_status(
            obj=self.payment)

        self.status = status
        self.payment.state = status
        self.payment.save()
