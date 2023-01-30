from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

# Not working yet


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "is_superuser",
    ]
    add_fieldsets = (
        (
            None,
            {"fields": ("username", "email", "password1", "password2")},
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
