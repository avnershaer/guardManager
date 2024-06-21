from django.contrib import admin
from .dal.models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.register(Families)
admin.site.register(Position)
admin.site.register(UserRole)
admin.site.register(SetGuardingList)
admin.site.register(Shift)
admin.site.register(GuardingList)
admin.site.register(Exchanges)
admin.site.register(PaidGuards)
admin.site.register(Fguard)



class UserRoleInLine(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = 'UserRole'
    fields = ('user_role', 'remark')


class CustomizedUserAdmin(UserAdmin):
    inlines = (UserRoleInLine,)



admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)





