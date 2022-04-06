from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage Users instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id", "email", "pseudo", "first_name", "last_name",
                    "is_staff")
    list_editable = ("email", "pseudo")
    search_fields = ("email", "pseudo", "first_name", "last_name")
    ordering = ('email',)


# Remove Groups from admin page
admin.site.unregister(Group)
