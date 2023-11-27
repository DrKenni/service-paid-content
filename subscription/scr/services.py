
import stripe


from config import settings
from subscription.models import Payment


class APIStripe:
    """Класс для работы с API Stripe"""

    def __init__(self):
        self.token = settings.STRIPE_API_KEY
        # stripe.api_key = self.token

    def create_product(self, name: str, price: int) -> dict:
        """Метод создает продукт в профиле используя API_KEY"""
        stripe.api_key = self.token
        data = {'unit_amount': price,
                "currency": 'usd'}

        product = stripe.Product.create(name=name)
        product_price = stripe.Price.create(
            unit_amount=price,
            currency='usd',
            product=product.stripe_id,
        )

        return {'stripe_product_id': product.stripe_id,
                'stripe_price_id': product_price.stripe_id}

    def get_payment_link(self, redirect_url: str, price_id: str) -> dict:
        """Создает сессию в stripe и возвращает словарь с сылкой на оплату"""
        stripe.api_key = self.token
        session = stripe.checkout.Session.create(
            success_url=redirect_url,
            line_items=[
                {
                    'price': price_id,
                    "quantity": 1
                }
            ],
            mode='payment',
        )
        return {'id': session['id'], 'url': session['url']}

    def get_status(self, obj):

        """Проверка статуса платежа"""
        stripe.api_key = self.token
        response = stripe.checkout.Session.retrieve(obj.stripe_id)
        payment = Payment.objects.get(stripe_id=obj.stripe_id)

        if response["payment_status"] == 'unpaid':
            payment.stripe_status = False
        else:
            payment.stripe_status = True
        payment.save()

    @staticmethod
    def delete_product(product_id: str) -> None:
        """Удаление продукт на стороне сервера stripe"""
        if product_id:
            stripe.Product.modify(product_id,
                                  active=False)
