from django.contrib import admin
from userlogin.models import chainYenClassInfo,UserAccountInfo, UserAccountAmwayInfo, UserAccountChainYenInfo, amwayAwardInfo
from userlogin.models import registerDDandDimInfo,AccountModifyHistory,\
    ConfirmString,chainYenJobTitleInfo,loginHistory
from userlogin.models import TempUserAccountInfo,TempUserAccountAmwayInfo,TempUserAccountChainYenInfo
from django.utils.translation import gettext_lazy
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#帳號管理相關

class UserAccountAmwayInfoInline(admin.StackedInline):
    model = UserAccountAmwayInfo
    extra = 0
    max_num = 0
class UserAccountChainYenInfoInline(admin.StackedInline):
    model = UserAccountChainYenInfo
    extra = 0
    max_num = 0
class usrloginAdmin(BaseUserAdmin):
    list_display = ('username','get_amwayNumber','user','last_login','is_superuser','is_staff','is_active','dataPermissionsLevel')
    fieldsets = (
        (None,{'fields':('username','password','first_name','last_name','email','dataPermissionsLevel')}),

        (gettext_lazy('User Information'), {'fields': ('user', 'phone', 'gender')}),

        (gettext_lazy('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active',
                                                  'groups', 'user_permissions')}),

        (gettext_lazy('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [
        UserAccountAmwayInfoInline,
        UserAccountChainYenInfoInline,
    ]

    def get_amwayNumber(self, obj):
        try:
            return "".join([str(k.amwayNumber) for k in obj.useraccountamwayinfo_set.all()])
        except:
            return "null"

    search_fields = ['username', 'user']
    get_amwayNumber.short_description = '會員編號'

class UserAccountAmwayInfoAdmin(admin.ModelAdmin):
    list_display = ('UserAccountInfo','get_name', 'amwayNumber', 'amwayAward','amwayDD')
    search_fields = ['amwayNumber','UserAccountInfo__user']
    list_filter = ('amwayDD','amwayAward')

    def get_name(self, obj):
        return obj.UserAccountInfo.user
    get_name.admin_order_field = 'UserAccountInfo__user'  # Allows column order sorting
    get_name.short_description = '姓名'  # Renames column head

class UserAccountChainYenInfoAdmin(admin.ModelAdmin):
    list_display = ('UserAccountInfo', 'get_name','jobTitle', 'classRoom','EM','point')
    search_fields = ['UserAccountInfo__username','UserAccountInfo__user']
    list_filter = ('jobTitle', 'classRoom','EM')
    def get_name(self, obj):
        return obj.UserAccountInfo.user
    get_name.admin_order_field = 'UserAccountInfo__user'  # Allows column order sorting
    get_name.short_description = '姓名'  # Renames column head
#帳號管理相關END
class amwayAwardInfoAdmin(admin.ModelAdmin):
    list_display = ('amwayAward', 'rank')

class chainYenClassInfoAdmin(admin.ModelAdmin):
    list_display = ('ClassRoomName', 'ClassRoomCode', 'rank')

class registerDDandDimInfoAdmin(admin.ModelAdmin):
    list_display = ('main','sec','amwayAward', 'amwayNumber', 'amwayDiamond')
    search_fields = ['main', 'amwayNumber','sec']
    list_filter = ('amwayAward', 'amwayDiamond')

class AccountModifyHistoryAdmin(admin.ModelAdmin):
    list_display = ('UserAccountInfo','get_name','recordDate','modifyFielddName', 'originFieldData','RevisedData', 'modifier')
    search_fields = ['UserAccountInfo__user', 'UserAccountInfo__username']
    list_filter = ('modifyFielddName',)
    def get_name(self, obj):
        return obj.UserAccountInfo.user
    get_name.admin_order_field = 'UserAccountInfo__user'  # Allows column order sorting
    get_name.short_description = '被變更者姓名'  # Renames column head
#註冊臨時表相關
class TempUserAccountAmwayInfoInline(admin.StackedInline):
    model = TempUserAccountAmwayInfo
    extra = 0
    max_num = 0
class TempUserAccountChainYenInfoInline(admin.StackedInline):
    model = TempUserAccountChainYenInfo
    extra = 0
    max_num = 0
class TempUserAccountInfoAdmin(admin.ModelAdmin):
    list_display = ('username','user', 'gender', 'phone','email','dataPermissionsLevel','auditStatus')
    search_fields = ['username','user']
    list_filter = ('auditStatus',)
    inlines = [
        TempUserAccountAmwayInfoInline,
        TempUserAccountChainYenInfoInline,
    ]

class TempUserAccountAmwayInfoAdmin(admin.ModelAdmin):
    list_display = ('UserAccountInfo','get_name', 'amwayNumber', 'amwayAward','amwayDD')
    search_fields = ['amwayNumber','UserAccountInfo__user']
    list_filter = ('amwayDD','amwayAward')

    def get_name(self, obj):
        return obj.UserAccountInfo.user
    get_name.admin_order_field = 'UserAccountInfo__user'  # Allows column order sorting
    get_name.short_description = '姓名'  # Renames column head
#
class TempUserAccountChainYenInfoAdmin(admin.ModelAdmin):
    list_display = ('UserAccountInfo', 'get_name','jobTitle', 'classRoom','EM','point')
    search_fields = ['UserAccountInfo__username','UserAccountInfo__user']
    list_filter = ('jobTitle', 'classRoom','EM')
    def get_name(self, obj):
        return obj.UserAccountInfo.user
    get_name.admin_order_field = 'UserAccountInfo__user'  # Allows column order sorting
    get_name.short_description = '姓名'  # Renames column head

class ConfirmStringAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'c_time', 'code')
    search_fields = ['user_name']

class chainYenJobTitleInfoAdmin(admin.ModelAdmin):
    list_display = ('jobTitle', 'rank')
    search_fields = ['jobTitle']

class loginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date','ip')
    search_fields = ['user']
# Register your models here.
admin.site.register(UserAccountInfo,usrloginAdmin)
admin.site.register(UserAccountAmwayInfo,UserAccountAmwayInfoAdmin)
admin.site.register(UserAccountChainYenInfo,UserAccountChainYenInfoAdmin)
admin.site.register(amwayAwardInfo,amwayAwardInfoAdmin)
admin.site.register(chainYenClassInfo,chainYenClassInfoAdmin)
admin.site.register(registerDDandDimInfo,registerDDandDimInfoAdmin)
admin.site.register(AccountModifyHistory,AccountModifyHistoryAdmin)
admin.site.register(TempUserAccountInfo,TempUserAccountInfoAdmin)
admin.site.register(TempUserAccountAmwayInfo,TempUserAccountAmwayInfoAdmin)
admin.site.register(TempUserAccountChainYenInfo,TempUserAccountChainYenInfoAdmin)
admin.site.register(ConfirmString,ConfirmStringAdmin)
admin.site.register(chainYenJobTitleInfo,chainYenJobTitleInfoAdmin)
admin.site.register(loginHistory,loginHistoryAdmin)