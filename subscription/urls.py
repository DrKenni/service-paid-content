from subscription.apps import SubscriptionConfig
from django.urls import path

from subscription.views import profile_follow, profile_unfollow, PaymentCheckView, PaymentCreateView

app_name = SubscriptionConfig.name

urlpatterns = [
    # Subscribe
    path('subscribe/<int:pk>/', profile_follow, name='subscribe'),
    path('unsubscribe/<int:pk>/', profile_unfollow, name='unsubscribe'),
    # Payment
    path('payment/check/<int:pk>/', PaymentCheckView.as_view(), name='check'),
    path('payment/<int:pk>/', PaymentCreateView.as_view(), name='payment'),
]
