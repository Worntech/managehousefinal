from django.contrib import admin
from .  models import *
from .models import Room, MyPayment

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class MyUserAdmin(BaseUserAdmin):
    list_display=('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_admin', 'is_active')
    search_fields=('email', 'first_name', 'last_name')
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    ordering=('email',)

# Register your models here.
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Contact)

admin.site.register(Room)
admin.site.register(MyPayment)
admin.site.register(Payment)