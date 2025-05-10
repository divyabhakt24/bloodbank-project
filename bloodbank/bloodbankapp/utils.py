# bloodbankapp/utils.py
from django.contrib.auth.models import User

def get_user_display_name(user):
    """Safe way to get a user's display name"""
    if user.first_name and user.last_name:
        return f"{user.first_name} {user.last_name}"
    return user.username