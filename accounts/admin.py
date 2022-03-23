from django.contrib import admin
from .models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage Users instances in the Admin
    interface.
    """
    list_display = ("id", "email", "first_name", "last_name", "is_staff")
    list_editable = ("email",)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
