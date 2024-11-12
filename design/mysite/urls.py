from django.urls import path, include
from .views import register, index, logout_user, login_user, create_application, app_created

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('create/', create_application, name='create_app'),
    path('app-created/', app_created, name='app_created'),
]