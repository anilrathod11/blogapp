from django.contrib import admin
from .models import CustomeUser


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'auth_provider','role']

admin.site.register(CustomeUser, UserAdmin)