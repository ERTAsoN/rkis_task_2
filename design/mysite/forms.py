from cProfile import label
from dataclasses import fields

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.shortcuts import get_object_or_404

from .models import User, DesignApplication, Category
import re

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=200, label='', widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    email = forms.CharField(required=True, max_length=200, label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(required=True, max_length=20, label='', widget=forms.TextInput(attrs={'placeholder': 'Телефон'}))
    last_name = forms.CharField(required=True, max_length=200, label='', widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    first_name = forms.CharField(required=True, max_length=200, label='', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    patronymic = forms.CharField(required=False, max_length=200, label='', widget=forms.TextInput(attrs={'placeholder': 'Отчество (если есть)'}))
    password = forms.CharField(required=True, max_length=200, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password_confirm = forms.CharField(required=True, max_length=200, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля'}))
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
    username = forms.CharField(required=True, max_length=200, label='', widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    password = forms.CharField(required=True, max_length=200, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

class CreateApplicationForm(forms.ModelForm):
    title = forms.CharField(required=True, max_length=200, label='', widget=forms.TextInput(attrs={'placeholder': 'Название'}))
    description = forms.CharField(required=True, max_length=200, label='', widget=forms.Textarea(attrs={'placeholder': 'Описание'}))
    photo = forms.FileField(required=True, label='Фото помещения', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])])

    class Meta:
        model = DesignApplication
        fields = ['title', 'description', 'category', 'photo']
        widgets = {'category':  forms.CheckboxSelectMultiple()}

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo.size > 1024*1024*2:
            raise ValidationError('Файл слишком большой. Размер не должен превышать 2 МБ.')
        return photo

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        app = super().save(commit=False)
        if self.user:
            app.creator = self.user

        if commit:
            app.save()
            self.save_m2m()
        return app


class EditAppForm(forms.ModelForm):
    design_comment = forms.CharField(required=False, max_length=200, label='', widget=forms.Textarea(attrs={'placeholder': 'Комментарий'}))
    design_photo = forms.FileField(required=False, label='Изображение дизайна', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])])
    discount = forms.IntegerField(min_value=0, max_value=100, label='Скидка')

    class Meta:
        model = DesignApplication
        fields = ['status', 'discount', 'design_comment', 'design_photo']
        widgets = { 'category': forms.CheckboxSelectMultiple(), }

    def clean_design_comment(self):
        new_status = self.cleaned_data.get('status')
        design_comment = self.cleaned_data.get('design_comment')
        if new_status == 'w' and not design_comment:
            raise ValidationError('Комментарий должен быть заполнен.')
        return design_comment

    def clean_design_photo(self):
        new_status = self.cleaned_data.get('status')
        design_photo = self.cleaned_data.get('design_photo')
        if new_status == 'd' and not design_photo:
            raise ValidationError('Изображение должно быть заполнено.')
        return design_photo

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        new_status = self.cleaned_data.get('status')
        if new_status == 'd':
            return discount
        return 0

class AppFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'Все'),
        ('n', 'Новая'),
        ('w', 'Принято в работу'),
        ('d', 'Выполнено'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label='Статус')