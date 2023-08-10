from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ViewCounter

UserAdmin.fieldsets[2][1]['fields'] = (
    "is_active",
    "is_staff",
    "is_superuser",
    "special_user",
    "groups",
    "user_permissions",
)

UserAdmin.list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_special_user")

admin.site.register(User, UserAdmin)
admin.site.register(ViewCounter)
