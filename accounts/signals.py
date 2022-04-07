from smtplib import SMTPDataError

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from bloodeal.settings import DEFAULT_FROM_EMAIL
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def send_email_after_new_user_signup(sender, instance, **kwargs):
    if instance.email and not instance.last_login:
        try:
            send_mail("[BLOODEAL] Nouvelle inscription",
                      f"Un utilisateur avec l'adresse email {instance.email} vient"
                      f" de s'inscrire.",
                      from_email=DEFAULT_FROM_EMAIL,
                      recipient_list=["jpvincent@hotmail.fr"],
                      fail_silently=False)
        except (SMTPDataError, ) as err:
            print("Envoi d'email suite à inscription impossible -> ", err)
