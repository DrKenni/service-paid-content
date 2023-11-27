from subscription.scr.services import APIStripe
from users.models import SubPlan


def task_create_product(pk):
    """Отложеная задача по созданию продукта"""
    stripe_api = APIStripe()
    plan = SubPlan.objects.get(pk=pk)
    data_id = stripe_api.create_product(name=plan.name,
                                        price=plan.price)
    plan.stripe_product_id = data_id['stripe_product_id']
    plan.stripe_price_id = data_id['stripe_price_id']
    plan.save()


def task_delete_product(product_id):
    APIStripe().delete_product(product_id)
