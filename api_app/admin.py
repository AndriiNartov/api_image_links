from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, AccountTier, Image, ExpiredLink, ThumbnailType


class MyUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'is_staff', 'is_active', 'account_tier', )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'account_tier',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )


admin.site.register(User, MyUserAdmin)


@admin.register(AccountTier)
class AccountTierAdmin(admin.ModelAdmin):
    model = AccountTier


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    model = Image


@admin.register(ExpiredLink)
class ExpiredLinkAdmin(admin.ModelAdmin):
    model = ExpiredLink



@admin.register(ThumbnailType)
class ThumbnailTypeLinkAdmin(admin.ModelAdmin):
    model = ThumbnailType


