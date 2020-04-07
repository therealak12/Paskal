from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['email', 'name']
    ordering = ('name',)
    search_fields = ('name', 'email',)

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal Info'), {'fields': ('name', 'bio', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
        (_('Personal Info'), {'fields': ('name', 'bio', 'avatar')}),
    )


admin.site.register(User, UserAdmin)
