from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.models import Profile


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30, min_length=3, required=True, label="Имя пользователя")
    email = forms.EmailField(max_length=100, required=True, label="Email")
    tel = forms.CharField(max_length=12, required=True, label="Номер телефона")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Подтверждение пароля")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile = Profile.objects.get(user=user)
            profile.tel = self.cleaned_data["tel"]
            profile.save()
        return user