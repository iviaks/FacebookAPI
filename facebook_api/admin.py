from django.contrib import admin

from .models import FacebookLabel, FacebookPage, FacebookUser


@admin.register(FacebookLabel)
class FacebookLabelAdmin(admin.ModelAdmin):
    pass


@admin.register(FacebookPage)
class FacebookPageAdmin(admin.ModelAdmin):
    pass


@admin.register(FacebookUser)
class FacebookUserAdmin(admin.ModelAdmin):
    pass
