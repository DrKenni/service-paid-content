from django import forms

from subscription.models import Subscription
from users.forms import StyleFormMixin


class PaidSubForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Subscription
        fields = '__all__'
