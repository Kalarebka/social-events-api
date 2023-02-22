from django.contrib import admin

from .models import Message


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


admin.site.register(Message, MessageAdmin)
