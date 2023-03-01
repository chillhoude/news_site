from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'is_staff', 'is_active','is_journalist','reputation')
    fieldsets = (
        ('Account', {'fields': ('username','password','avatar')}),
        ('Personal Data', {'fields': ('first_name','last_name','reputation', 'email')}),
        ('Permissions', {'fields': ('is_journalist','is_staff', 'is_active')}),
        ('Date', {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff','is_journalist', 'is_active')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
