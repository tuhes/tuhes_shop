from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view')
]