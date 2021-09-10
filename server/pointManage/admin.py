from django.contrib import admin
from pointManage.models import pointHistory
# Register your models here.

class pointHistoryAdmin(admin.ModelAdmin):
    list_display = ('UserAccountInfo',
                    'get_name',
                    'recordDate',
                    'reason',
                    'addPoint',
                    'reducePoint',
                    'transferPoint',
                    'resultPoint',
                    'modifier',
                    )
    search_fields = ['UserAccountInfo__username','UserAccountInfo__user']
    def get_name(self, obj):
        return obj.UserAccountInfo.user
    get_name.admin_order_field = 'UserAccountInfo__user'  # Allows column order sorting
    get_name.short_description = '被變更者姓名'  # Renames column head

admin.site.register(pointHistory,pointHistoryAdmin)