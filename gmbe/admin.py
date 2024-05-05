from django.contrib import admin
from .dal.models import *


admin.site.register(Families)
admin.site.register(Position)
admin.site.register(UserRole)
admin.site.register(SetGuardingList)
admin.site.register(Shift)
admin.site.register(GuardingList)
