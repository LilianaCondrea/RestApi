from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile
from .filters import AgeStatusListFilter, UpdateStatusListFilter


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name',)
    list_per_page = 20
    list_filter = ('gender', AgeStatusListFilter, UpdateStatusListFilter)
    search_fields = ('first_name', 'last_name')
    ordering = ('-last_update',)

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_superuser")
    search_fields = ("username", "email")
    list_per_page = 20
    list_filter = ('is_superuser', 'is_staff', 'last_login',)
    ordering = ('-last_login',)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
