from django.contrib import admin

from users.models import User, SubPlan

admin.site.register(User)


@admin.register(SubPlan)
class SubPlanAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'length', 'price')
    list_filter = ('owner', 'name', 'length', 'price')
