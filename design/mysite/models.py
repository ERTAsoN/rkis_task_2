from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=200, verbose_name='Имя пользователя', unique=True)
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=200, verbose_name='Отчество')
    email = models.EmailField(max_length=200, verbose_name='Email', unique=True)
    password = models.CharField(max_length=200, verbose_name='Пароль')
    phone = models.CharField(max_length=20, verbose_name='Телефон', default='0000000000')

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class DesignApplication(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Создатель')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Описание')
    photo = models.FileField(verbose_name='Фото помещения')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    CATEGORY = (
        ('l', 'Жилые помещения'),
        ('c', 'Коммерческие помещения'),
        ('h', 'Отели и гостиницы'),
        ('b', 'Бары и клубы'),
        ('s', 'Спа-салоны и салоны красоты'),
        ('m', 'Медицинские учреждения'),
        ('o', 'Общественные здания'),
        ('g', 'Cадовые домики и загородные дома'),
    )

    APP_STATUS = (
        ('n', 'Новая'),
        ('w', 'Принято в работу'),
        ('d', 'Выполнена'),
    )

    category = models.CharField(max_length=1, verbose_name='Категория', choices=CATEGORY, blank=True, default='l')
    status = models.CharField(max_length=1, verbose_name='Статус заявки', choices=APP_STATUS, blank=True, default='n')

    def __str__(self):
        return self.title

    def time_created_f(self):
        return self.time_created