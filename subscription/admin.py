from django.contrib import admin

from subscription.models import Subscription, PaidSubscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('owner', 'creator')
    list_filter = ('owner', 'creator')


@admin.register(PaidSubscription)
class PaidSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('owner', 'creator')
    list_filter = ('owner', 'creator')
