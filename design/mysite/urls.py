from django.urls import path, include
from .views import register, index, login

urlpatterns = [
    path('', index, name='index'),
    path('accounts/register/', register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]