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

class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название', unique=True)
    price = models.IntegerField(verbose_name='Цена', default=0)

    def __str__(self):
        return f'{self.title} - {self.price}'

class DesignApplication(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Создатель')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Описание')
    photo = models.FileField(verbose_name='Фото помещения')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.ManyToManyField(Category, null=False, verbose_name='Категория')
    discount = models.IntegerField(verbose_name='Скидка', default=0)
    payment_confirmed = models.BooleanField(verbose_name='Оплата произведена', default=False)

    design_comment = models.TextField(max_length=1000, verbose_name='Комментарий', blank=True)
    design_photo = models.FileField(verbose_name='Изображение дизайна', blank=True)

    APP_STATUS = (
        ('n', 'Новая'),
        ('w', 'Принято в работу'),
        ('d', 'Выполнена'),
    )

    status = models.CharField(max_length=1, verbose_name='Статус заявки', choices=APP_STATUS, null=False, default='n')

    class Meta:
        permissions = [
            ('can_edit_status', 'Can edit application status')
        ]

    def __str__(self):
        return self.title

    def time_created_f(self):
        return self.time_created

    def get_category(self):
        categories = self.category.all()[:1]
        return ', '.join(str(category.title) for category in categories)

    def get_categories(self):
        categories = self.category.all()
        return ', '.join(str(category.title) for category in categories)

    def get_price(self):
        categories = self.category.all()
        return int(sum(category.price for category in categories) * (100 - self.discount) / 100)