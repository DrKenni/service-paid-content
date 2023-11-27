from django import forms

from blog.models import Article
from blog.services import ReExpression
from users.forms import StyleFormMixin


class ArticleForm(StyleFormMixin, forms.ModelForm):
    """Форма описывающая посты"""

    banned_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                    'бесплатно', 'обман', 'полиция', 'радар']

    def save(self, commit=True):
        """Переопределение для добавления video_id во время сохранения"""

        self.instance = super().save(commit=False)
        video_id = ReExpression.get_video_id(self.cleaned_data['video_url'])
        self.instance.video_url = f'https://www.youtube.com/embed/{video_id}'
        self.instance.save()
        return self.instance

    def clean_title(self):
        """Проверка на наличие запрещенных слов в загаловке"""
        cleaned_data = self.cleaned_data['title']
        for word in self.banned_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('В названии есть запрещенные слова!')
        return cleaned_data

    def clean_content(self):
        """Проверка на наличие запрещенных слов в тексте"""
        cleaned_data = self.cleaned_data['content']
        for word in self.banned_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('В описании есть запрещенные слова!')
        return cleaned_data

    def clean_video_url(self):
        """Проверка на url"""
        cleaned_data = self.cleaned_data.get('video_url')
        if cleaned_data:
            if ReExpression.check_url(cleaned_data) is False:
                raise forms.ValidationError('Видео должно быть с youtube.com.')

            return cleaned_data

    class Meta:
        model = Article
        fields = ('title',
                  'content',
                  'image',
                  'is_published',
                  'is_sub',
                  'video_url')
        help_texts = {
            'content': 'Ваше сообщение миру.',
            'is_sub': 'Контент только для подписчиков на платной основе',
            'is_published': 'Пост будет доступен отовсюду или только в вашем профиле',
            'video_url': 'Можно добавить сылку на видео с youtube.com'
        }
