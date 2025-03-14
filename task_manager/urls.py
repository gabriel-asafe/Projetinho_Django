
from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
    path('projects/', include('projects.urls')),

]