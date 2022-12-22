from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# do I need a custom UserAdmin for a custom user?

admin.site.register(User, UserAdmin)
