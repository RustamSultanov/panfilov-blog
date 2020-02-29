from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
import wagtail.users.models


# Now register the new UserAdmin# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Users'


class WagtailUserProfileInline(admin.StackedInline):
    model = wagtail.users.models.UserProfile
    can_delete = False
    verbose_name_plural = 'WagtailUsers'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, WagtailUserProfileInline)


# Re-register UserAdmin
admin.site.register(Shop)
admin.site.register(Task)
admin.site.register(Department)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Messeges)
admin.site.register(Feedback)
