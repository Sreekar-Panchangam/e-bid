from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from miniproject.views import HomePage

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
