from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('id','password')
    ordering = ('created_at',)
    filter_horizontal = ()
    list_filter = ('is_admin','is_staff')
    fieldsets = ()
admin.site.register(Account,AccountAdmin)