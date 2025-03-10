from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:profile_view')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login_view')


'''def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:profile_view')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})'''


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login_view')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})


@login_required(login_url='accounts:login_view')
def profile_view(request):
    return render(request, 'registration/profile.html')
