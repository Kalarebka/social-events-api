from django.contrib import admin

from .models import Message, MessageThread


class MessageAdmin(admin.ModelAdmin):
    list_display = ("title", "date_sent", "sender_username", "receiver_username")
    list_filter = ("sender", "receiver")
    search_fields = ("title", "sender__username", "receiver__username")

    def sender_username(self, obj):
        return obj.sender.username

    def receiver_username(self, obj):
        return obj.receiver.username

    sender_username.short_description = "From:"
    receiver_username.short_description = "To:"


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


class MessageThreadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_user1_name",
        "get_user2_name",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("user1__username", "user2__username")
    inlines = [MessageInline]

    def get_user1_name(self, obj):
        return obj.user1.username

    get_user1_name.admin_order_field = "user1__username"
    get_user1_name.short_description = "User 1"

    def get_user2_name(self, obj):
        return obj.user2.username

    get_user2_name.admin_order_field = "user2__username"
    get_user2_name.short_description = "User 2"


admin.site.register(Message, MessageAdmin)
admin.site.register(MessageThread, MessageThreadAdmin)
