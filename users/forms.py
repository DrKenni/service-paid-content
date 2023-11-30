from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from django import forms

from subscription.scr.services import APIStripe
from users.models import User, SubPlan, Verify
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
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'без +7 и пробелов, например: 999 222 11 33'}))

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
    about_me = forms.CharField(label='About me',
                               widget=forms.TextInput(attrs={'class': 'form-input'}),
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
    price = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Цена должны быть целым числом без знака "." и ","'}))

    def save(self, commit=True):
        """Создание продукта"""

        self.instance.save()
        # task_create_product.delay(pk=self.instance.pk)
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


class VerifyForm(forms.ModelForm):

    def clean(self):
        clean_data = super().clean()
        user_input = clean_data.get('user_input')
        if int(user_input) != self.instance.code:
            raise forms.ValidationError('Код неверен')

        return clean_data

    class Meta:
        model = Verify
        fields = ('user_input',)


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')
