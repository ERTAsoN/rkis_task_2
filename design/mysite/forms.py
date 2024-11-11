from django import forms
from django.core.exceptions import ValidationError
from .models import User
import re

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=200, label='Имя пользователя', widget=forms.TextInput())
    email = forms.CharField(required=True, max_length=200, label='Email', widget=forms.TextInput())
    phone = forms.CharField(required=True, max_length=20, label='Телефон', widget=forms.TextInput())
    last_name = forms.CharField(required=True, max_length=200, label='Фамилия', widget=forms.TextInput())
    first_name = forms.CharField(required=True, max_length=200, label='Имя', widget=forms.TextInput())
    patronymic = forms.CharField(max_length=200, label='Отчество (если есть)',  widget=forms.TextInput())
    password = forms.CharField(required=True, max_length=200, label='Пароль', widget=forms.PasswordInput)
    password_confirm = forms.CharField(required=True, max_length=200, label='Подтверждение пароля', widget=forms.PasswordInput)
    consent = forms.BooleanField(required=True, label='Согласие на обработку персональных данных', widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'last_name', 'first_name', 'patronymic', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Данное имя пользователя уже занято.')
        if not re.match(r'^[A-z-]+$', username):
            raise ValidationError('Имя пользователя должно содержать только латиницу и дефисы.')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[А-яёЁ\s-]+$', first_name):
            raise ValidationError('ФИО должно содержать только кириллицу, пробелы и дефисы.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[А-яёЁ\s-]+$', last_name):
            raise ValidationError('ФИО должно содержать только кириллицу, пробелы и дефисы.')
        return last_name

    def clean_patronymic(self):
        patronymic = self.cleaned_data.get('patronymic')
        if not re.match(r'^[А-яёЁ\s-]+$', patronymic):
            raise ValidationError('ФИО должно содержать только кириллицу, пробелы и дефисы.')
        return patronymic

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError('Пароли должны совпадать.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=200)
    password = forms.CharField(required=True, max_length=200, widget=forms.PasswordInput)