from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, \
    forms
from django.conf import settings

from accounts.models import CustomUser


class SignupForm(UserCreationForm):
    """
    A form inheriting from UserCreationForm to create a CustomUser instance.
    """
    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]
        widgets = {"email": forms.fields.TextInput(attrs={"placeholder": "email"})}
        error_messages = [{"email": "Cet email existe déjà."}]


class LoginForm(AuthenticationForm):
    """
    A form inheriting from AuthenticationForm for users to login.
    """
    pass
