from catalog.models import Review
from django import forms
from mixin.recaptcha_mixin import ReCaptchaMixin


class ReviewForm(ReCaptchaMixin, forms.ModelForm):

    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 25, 'placeholder': 'Напишите свой отзыв...'}),
            'rating': forms.RadioSelect(),
        }
        labels = {
            'text': 'Отзыв',
            'rating': 'Рейтинг'
        }