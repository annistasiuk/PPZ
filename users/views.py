from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import UserRegistrationForm, UserLoginForm


def user_login_view(request):
    """Використовується для входу користувача в систему. Перенаправляє на головну сторінку."""
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('songs:index'))
    else:
        form = UserLoginForm(request)
    return render(request, 'users/login.html', {'form': form})


def user_registration_view(request):
    """Використовується для реєстрації користувача. Перенаправляє на сторінку входу."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def user_logout_view(request):
    """Використовується для виходу користувача з системи. Перенаправляє на головну сторінку."""
    if request.method == 'POST':
        logout(request)
    return redirect(reverse('songs:index'))
