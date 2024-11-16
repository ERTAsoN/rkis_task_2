from unicodedata import category

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView, UpdateView, CreateView

from django import forms
from .forms import RegistrationForm, LoginForm, CreateApplicationForm, EditAppForm, AppFilterForm
from .models import DesignApplication, Category


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

@login_required
def create_application(request):
    if request.method == 'POST':
        form = CreateApplicationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()  # Saves the instance with correct category
            return redirect('account')
        else:
            print(form.errors)  # Print out the errors for debugging
    else:
        form = CreateApplicationForm()
    return render(request, 'create_app.html', {'form': form})

class AccountListView(LoginRequiredMixin, generic.ListView):
    model = DesignApplication
    template_name = 'account.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')

        if status:
            queryset = queryset.filter(status=status)

        queryset = queryset.order_by('-time_created')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = AppFilterForm(self.request.GET or None)
        return context

class HomepageListView(generic.ListView):
    model = DesignApplication
    template_name = 'index.html'

    def get_queryset(self):
        return DesignApplication.objects.all().filter(status='d').order_by('-time_created')[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apps_in_process'] = DesignApplication.objects.filter(status='w').count()
        return context

class AllAppsListView(generic.ListView, PermissionRequiredMixin):
    permission_required = 'mysite.can_edit_status'
    model = DesignApplication
    template_name = 'all_apps.html'

    def get_queryset(self):
        return DesignApplication.objects.all().order_by('-time_created')

class AllCategoriesListView(generic.ListView, PermissionRequiredMixin):
    permission_required = 'mysite.can_edit_status'
    model = Category
    template_name = 'all_categories.html'

    def get_queryset(self):
        return Category.objects.all().order_by('id')

class AppDelete(DeleteView, LoginRequiredMixin):
    model = DesignApplication
    success_url = reverse_lazy('account')
    template_name = 'delete_app.html'

    def get_queryset(self):
        return super().get_queryset()

class CategoryDelete(DeleteView, PermissionRequiredMixin):
    permission_required = 'mysite.can_edit_status'
    model = Category
    success_url = reverse_lazy('all_categories')
    template_name = 'delete_category.html'

    def get_queryset(self):
        return super().get_queryset()

class EditApp(UpdateView, PermissionRequiredMixin):
    permission_required = 'mysite.can_edit_status'
    model = DesignApplication
    template_name = 'edit_app.html'
    form_class = EditAppForm

    success_url = reverse_lazy('all_apps')

class EditAppDone(UpdateView, PermissionRequiredMixin):
    permission_required = 'mysite.can_edit_status'
    model = DesignApplication
    template_name = 'edit_app_done.html'
    fields = ['payment_confirmed']

    success_url = reverse_lazy('all_apps')

class EditCategory(UpdateView, PermissionRequiredMixin):
    permission_required = 'mysite.can_edit_status'
    model = Category
    template_name = 'edit_category.html'
    fields = ['title', 'price']

    success_url = reverse_lazy('all_categories')

class CreateCategory(CreateView, PermissionRequiredMixin):
    permission_required = 'mysite.can_edit_status'
    model = Category
    template_name = 'create_category.html'
    fields = ['title', 'price']

    success_url = reverse_lazy('all_categories')