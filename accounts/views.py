from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm
from .models import User
from wallet.models import Wallet

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        Wallet.objects.create(user=user)
        return redirect('accounts:login')

class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('home')

class DashboardView(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'accounts/dashboard.html'
    fields = ['first_name', 'last_name', 'email', 'mobile_no', 'address', 'city', 'state', 'pincode', 'profile_picture']

    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')

    def get_object(self):
        return self.request.user

class LogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = reverse_lazy('home')
