from django.contrib import admin

from .models import Deal


# Register your models here.
@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage BluRay instances in the Admin
    interface.
    """
    list_display = ("id", "blu_ray", "created_by", "status", "price")
    list_editable = ("blu_ray", "created_by", "status", "price")
    search_fields = ("blu_ray",)
    ordering = ("blu_ray",)
