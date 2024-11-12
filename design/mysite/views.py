from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, CreateApplicationForm


def index(request):
    return render(request, 'index.html')

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль.')

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_user(request):
    logout(request)
    return render(request, 'registration/logout.html')

def create_application(request):
    if request.method == 'POST':
        form = CreateApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app_created')
        else:
            print(form.errors)
    else:
        form = CreateApplicationForm()
    return render(request, 'create_application.html', {'form': form})

def app_created(request):
    return render(request, 'app_created.html')