from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib import admin
from .models import CustomUser

# base.py에 정의된 AUTH_USER_MODEL
User = get_user_model()


@admin.register(User)
class CustomUserAdmin(auth_admin.UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('user_id', 'username')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    list_display = ['email', 'user_id', 'username', 'is_active', 'is_staff']
    search_fields = ['email', 'user_id', 'username']
    ordering = ('email',)
    readonly_fields = ('last_login',)

    filter_horizontal = ()
    list_filter = ('is_active', 'is_staff')