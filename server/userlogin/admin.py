from django.contrib import admin
from userlogin.models import UserAccountInfo, UserAccountAmwayInfo , UserAccountChainYenInfo , amwayAwardInfo
from django.utils.translation import gettext_lazy
from django.contrib.auth.admin import UserAdmin

class usrloginAdmin(admin.ModelAdmin):
    list_display = ('username','last_login','is_superuser','is_staff','is_active','date_joined')
    fieldsets = (
        (None,{'fields':('username','password','first_name','last_name','email')}),

        (gettext_lazy('User Information'), {'fields': ('user', 'phone', 'gender')}),

        (gettext_lazy('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active',
                                                  'groups', 'user_permissions')}),

        (gettext_lazy('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

# Register your models here.
admin.site.register(UserAccountInfo,UserAdmin)
admin.site.register(UserAccountAmwayInfo)
admin.site.register(UserAccountChainYenInfo)
admin.site.register(amwayAwardInfo)
