from django.contrib.auth.forms import (
    forms,
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
    PasswordChangeForm)

from accounts.models import CustomUser


class SignupForm(UserCreationForm):
    """
    A form inheriting from UserCreationForm to create a CustomUser instance.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["email"].label = "EMAIL"
        self.fields["pseudo"].label = "PSEUDO"
        self.fields["password1"].label = "MOT DE PASSE"
        self.fields["password2"].label = "CONFIRMEZ VOTRE MOT DE PASSE"

    class Meta:
        model = CustomUser
        fields = ["email", "pseudo", "password1", "password2"]
        widgets = {"pseudo": forms.fields.TextInput(attrs={"placeholder": "Facultatif"})}
        error_messages = {
            "email": {
                "unique": "Un compte avec cette adresse email existe déjà."}
        }


class LoginForm(AuthenticationForm):
    """
    A form inheriting from AuthenticationForm for users to login.
    """
    # error_messages = [
    #     {"invalid_login": "Adresse email et/ou mot de passe non valide."},
    #     {"inactive": "Ce compte est inactif."}]
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.label_suffix = ""
        self.fields["username"].label = "EMAIL"
        self.fields["password"].label = "MOT DE PASSE"


class CustomUserChangeForm(UserChangeForm):
    """
    A form inheriting from UserChangeForm to update a CustomUser instance.
    """
    password = None

    def __init__(self, *args, **kwargs):
        if kwargs.get("user"):
            kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["email"].label = "EMAIL"
        self.fields["pseudo"].label = "PSEUDO"
        self.fields["first_name"].label = "PRENOM"
        self.fields["last_name"].label = "NOM"

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "pseudo"]
        error_messages = {
            "email": {
                "unique": "Un compte avec cette adresse email existe déjà."}
        }


class CustomUserChangePasswordForm(PasswordChangeForm):
    """
    A form inheriting from UserChangeForm to update a CustomUser instance.
    """
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.label_suffix = ""
        self.fields["old_password"].label = "MOT DE PASSE ACTUEL"
        self.fields["new_password1"].label = "NOUVEAU MOT DE PASSE"
        self.fields["new_password2"].label = "CONFIRMEZ LE NOUVEAU MOT DE PASSE"

    # def get_context(self):
    #     context = super(CustomUserChangePasswordForm, self).get_context()
    #     context["change_password_form"] = context["form2"]
    #     return context

    class Meta:
        model = CustomUser
        fields = ["old_password", "new_password1", "new_password2"]
