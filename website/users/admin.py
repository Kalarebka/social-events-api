from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

# Not working yet


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_form_template = "admin/auth/user/add_form.html"
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
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
