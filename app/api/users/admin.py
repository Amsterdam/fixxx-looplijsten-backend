from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.users.models import User, Team

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        ('None', {'fields': ('email', 'password', 'username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    model = Team
    filter_horizontal = ('members',)
