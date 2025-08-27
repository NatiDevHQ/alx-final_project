from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ["id", "username", "email", "name", "is_staff", "is_active"]
    search_fields = ["username", "email", "name"]

    # show `name` on edit page
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("name",)}),
    )
    # show `name` on add page
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("name",)}),
    )
