from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.backends import BaseBackend
from .models import User

class Backend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
                else:
                    return None
            except User.DoesNotExist:
                return None

    def get_user(request, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None