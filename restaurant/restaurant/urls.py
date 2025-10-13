from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from reservations import views as reservation_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', reservation_views.register, name='register'),
    path('', include('reservations.urls')),
]
