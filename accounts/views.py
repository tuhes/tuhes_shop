from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from orders.models import Order
import hashlib
import hmac
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User


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
    user = request.user
    active_orders = Order.objects.filter(user=user, status='active')
    completed_orders = Order.objects.filter(user=user, status='completed')
    canceled_orders = Order.objects.filter(user=user, status='canceled')

    orders = {
        'active_orders': active_orders,
        'completed_orders': completed_orders,
        'canceled_orders': canceled_orders,
    }

    return render(request, 'registration/profile.html', context=orders)


def verify_telegram_auth(data: dict, token: str) -> bool:
    auth_data = data.copy()
    hash_received = auth_data.pop('hash')
    secret_key = hashlib.sha256(token.encode()).digest()
    check_string = '\n'.join([f"{k}={v}" for k,v in sorted(auth_data.items())])
    hmac_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
    return hmac_hash == hash_received


def telegram_login_complete(request):
    data = request.GET.dict()

    if not verify_telegram_auth(data, settings.TELEGRAM_BOT_TOKEN):
        return HttpResponseBadRequest("Invalid hash")

    telegram_id = data.get('id')
    username = data.get('username')

    user, created = User.objects.get_or_create(username=username, defaults={'first_name': data.get("first_name")})

    if created:
        user.set_unusable_password()
        user.save()

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect('accounts:profile_view')
