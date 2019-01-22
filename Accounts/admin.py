from django.contrib import admin

# Register your models here.
from .models import Account,Shop, Product, Category, Campaign
from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User




@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','email','company_name','phone_number','documents', 'created')

admin.site.register(Account, AccountAdmin)

class ShopAdmin(admin.ModelAdmin):
    list_display = ('subdomain','shop_name','created', 'shop_balance', 'is_activated','paid')

admin.site.register(Shop,ShopAdmin)

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('fullname','email_address','phone_number','message')


admin.site.register(Campaign, CampaignAdmin)



admin.site.register(Product)
admin.site.register(Category)
