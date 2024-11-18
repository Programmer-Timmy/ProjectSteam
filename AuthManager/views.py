from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomLoginForm


# Login View
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard-index')  # Redirect to the home page or dashboard after login
            else:
                form.add_error(None, "Invalid username or password.")
        else:
            # If the form is invalid, it will automatically pass back errors to the template
            pass
    else:
        form = CustomLoginForm()

    return render(request, 'AuthManager/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('index')

# Register View
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'AuthManager/register.html', {'form': form})

