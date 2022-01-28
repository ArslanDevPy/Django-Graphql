from django.contrib import admin
from graphql_auth.models import UserStatus


# admin.site.register(UserStatus)

@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ['user', 'verified', 'archived', 'secondary_email']
