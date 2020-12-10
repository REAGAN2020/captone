

from django.contrib import admin
from .models import Services, Post, Comment, Review
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import *
from gari.models import User
from django.contrib.auth.admin import UserAdmin



##########


# admin.site.register(UserProfile)
admin.site.register(Services)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.unregister(Group)

admin.site.site_header = 'ReaganGarage Dashboard'
admin.site.site_title = 'Welcome to ReaganGarage Admin Dashboard'
admin.site.index_title = 'ReaganGarage Portal'

TEXT = 'section description'

class AccountAdmin(UserAdmin):
    list_display = ("email", "username", "date_joined", 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User,AccountAdmin)



