
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms

from subscription.scr.services import APIStripe
from users.models import User, SubPlan
from users.tasks import task_create_product


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class UserViewForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'surname',
                  'sex',
                  'email',
                  'password1',
                  'password2',
                  'phone')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    about_me = forms.CharField(label='About me', widget=forms.TextInput(attrs={'class': 'form-input'}),
                               required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'surname',
                  'about_me',
                  'avatar')


class SubPlanView(StyleFormMixin, forms.ModelForm):

    def save(self, commit=True):
        """Создание продукта"""

        self.instance.save()
        # task_create_product(self.instance.pk)
        stripe_api = APIStripe()
        plan = SubPlan.objects.get(pk=self.instance.pk)
        data_id = stripe_api.create_product(name=plan.name,
                                            price=plan.price)
        plan.stripe_product_id = data_id['stripe_product_id']
        plan.stripe_price_id = data_id['stripe_price_id']
        plan.save()
        return self.instance

    class Meta:
        model = SubPlan
        fields = ('name',
                  'price',
                  'length')
