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
                # if there is no steam id and the user is not opted out, redirect to steam login
                # if user.steam_id is None and not user.opt_out and not user.steam_opt_out:
                #     return redirect('connect_steam')
                # else:
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

    # if user is not opted out, connect to steam

    return render(request, 'AuthManager/register.html', {'form': form})

# Need Account View
def need_account(request):
    return render(request, 'AuthManager/need_account.html', {'title': 'Need Account'})

def connect_steam(request):
    if request.method == 'POST':
        user = request.user
        user.steam_opt_out = True
        user.save()
        return redirect('dashboard-index')

    return render(request, 'AuthManager/connect_steam.html', {'title': 'Connect Steam'})