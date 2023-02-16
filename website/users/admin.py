from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, UserGroup, FriendInvitation, GroupInvitation


class FromUserInline(admin.TabularInline):
    model = (
        CustomUser.friends.through
    )  # intermediate model for many-to-many relationship
    fk_name = "from_customuser"
    extra = 1  # num of extra empty lines shown to add


class ToUserInline(admin.TabularInline):
    model = CustomUser.friends.through
    fk_name = "to_customuser"
    extra = 1


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

    inlines = [FromUserInline, ToUserInline]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserGroup)
admin.site.register(FriendInvitation)
admin.site.register(GroupInvitation)
