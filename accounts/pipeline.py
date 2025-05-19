from django.contrib.auth import get_user_model
from models import Profile
from datetime import datetime

User = get_user_model()

def save_email_birthday(strategy, details, backend, user=None, *args, **kwargs):
    if user and backend.name == 'vk-oauth2':
        if details.get('email'):
            user.email = details.get('email')
            user.save()

        response = kwargs.get('response', {})
        bdate= response.get('bdate')

        if bdate:
            birthday= datetime.strptime(bdate, '%d-%m-%Y').date()
            user.profile.birth_date = birthday
            user.profile.save()
    return {}