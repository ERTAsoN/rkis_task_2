from django.urls import path

from .views import register, logout_user, login_user, create_application, AccountListView, HomepageListView, AppDelete, \
    AllAppsListView, EditApp, AllCategoriesListView, EditCategory, CategoryDelete, CreateCategory, EditAppDone

urlpatterns = [
    path('', HomepageListView.as_view(), name='index'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('create/', create_application, name='create_app'),
    path('all-apps/', AllAppsListView.as_view(), name='all_apps'),
    path('all-categories/', AllCategoriesListView.as_view(), name='all_categories'),
    path('account/', AccountListView.as_view(), name='account'),
    path('app/<int:pk>/delete/', AppDelete.as_view(), name='app_delete'),
    path('app/<int:pk>/edit/', EditApp.as_view(), name='app_edit'),
    path('app/<int:pk>/edit-done/', EditAppDone.as_view(), name='app_edit_done'),
    path('category/<int:pk>/edit/', EditCategory.as_view(), name='edit_category'),
    path('category/<int:pk>/delete/', CategoryDelete.as_view(), name='delete_category'),
    path('category/create/', CreateCategory.as_view(), name='create_category'),
]