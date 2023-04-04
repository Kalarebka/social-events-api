from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, FriendInvitation, GroupInvitation, UserGroup


class FromUserInline(admin.TabularInline):
    model = CustomUser.friends.through
    fk_name = "from_customuser"
    extra = 1


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


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "get_admins", "num_members")

    def get_admins(self, obj):
        return ", ".join([admin.username for admin in obj.administrators.all()])

    get_admins.short_description = "Admins"

    def num_members(self, obj):
        return obj.members.count()

    num_members.short_description = "Number of members"


class FriendInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "sender",
        "recipient",
        "confirmed",
        "response_received",
        "date_sent",
        "status",
    )
    search_fields = (
        "sender__username",
        "recipient__username",
    )

    def status(self, obj):
        if obj.confirmed:
            return "confirmed"
        elif obj.response_received:
            return "declined"
        else:
            return "pending"

    status.short_description = "Status"


class GroupInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "group",
        "recipient",
        "confirmed",
        "response_received",
        "date_sent",
        "status",
    )
    search_fields = (
        "group__name",
        "recipient__username",
    )

    def status(self, obj):
        status_dict = {
            (False, False): "pending",
            (True, False): "confirmed",
            (True, True): "declined",
        }
        return status_dict[(obj.confirmed, obj.response_received)]

    status.short_description = "Status"


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserGroup, UserGroupAdmin)
admin.site.register(FriendInvitation, FriendInvitationAdmin)
admin.site.register(GroupInvitation, GroupInvitationAdmin)
