from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, CreateApplicationForm
from .models import DesignApplication
from django.views import generic


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
        form = CreateApplicationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('app_created')
        else:
            print(form.errors)
    else:
        form = CreateApplicationForm()
    return render(request, 'create_app.html', {'form': form})

def app_created(request):
    return render(request, 'account.html')

class AppListView(LoginRequiredMixin, generic.ListView):
    model = DesignApplication
    template_name = 'account.html'

    def get_queryset(self):
        return DesignApplication.objects.filter(creator=self.request.user).order_by('-time_created')