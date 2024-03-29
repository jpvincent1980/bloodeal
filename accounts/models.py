from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Define a model manager for CustomUser model with no username field.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a CustomUser with the given email and password."""

        if not email:
            raise ValueError('Vous devez saisir une adresse email valide.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular CustomUser with the given email and
        password.
        """

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    A model that represents a user
    """

    username = None
    first_name = models.CharField(max_length=200,
                                  blank=True,
                                  null=True)
    last_name = models.CharField(max_length=200,
                                 blank=True,
                                 null=True)
    email = models.EmailField(unique=True)
    pseudo = models.CharField(max_length=24,
                              blank=True,
                              null=True,
                              unique=True,
                              error_messages={'unique': 'Ce pseudo est déjà pris.'})

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:

        verbose_name = "Utilisateur"

    def __str__(self):

        name = self.pseudo if self.pseudo else self.email

        return f"{name}"

    def join_date(self):
        return self.date_joined.strftime("%d/%m/%Y")
