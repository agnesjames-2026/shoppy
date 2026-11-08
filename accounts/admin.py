'''from django.contrib import admin
from .models import Account
# Register your models here.

admin.site.register(Account)
'''


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'username',
        'last_login',
        'is_staff',
        'is_active',
        
    )
    list_display_links=('email','first_name','last_name')
    readonly_fields=('last_login','date_joined')

    ordering = ('date_joined',)
    search_fields = ('email', 'username')

    fieldsets = ()
    filter_horizontal = ()
    list_filter = ()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'username',
                'phone_number',
                'password1',
                'password2',
            ),
        }),
    )


admin.site.register(Account, AccountAdmin)
