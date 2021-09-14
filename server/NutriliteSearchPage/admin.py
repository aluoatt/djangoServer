from django.contrib import admin
from NutriliteSearchPage.models import fileDataInfo
from NutriliteSearchPage.models import DBClassInfo,mainClassInfo,secClassInfo,fileTypeInfo,\
    sourceFromInfo,fileDataKeywords
from NutriliteSearchPage.models import personalFileData,personalExchangeFileLog
# Register your models here.
class fileDataKeywordsInline(admin.StackedInline):
    model = fileDataKeywords

class fileDataInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('title',
                    'DBClass',
                    'mainClass',
                    'secClass',
                    'describe',
                    'fileType',
                    # 'characterName',
                    # 'characterClass',
                    'occurrenceDate',
                    'point',
                    'visible',
                    'needWaterMark',
                    'downloadAble',
                    'permissionsLevel',
                    'likes'
                    )

    search_fields = ['title','describe']
    list_filter = ('mainClass','secClass','fileType','downloadAble','needWaterMark','visible','characterClass',)
    inlines = [
        fileDataKeywordsInline,
    ]
    readonly_fields = ["likes",]

class DBClassInfoAdmin(admin.ModelAdmin):
    list_display = ('DBClassName',
                    'DBClassCode',
                    )

class fileDataKeywordsAdmin(admin.ModelAdmin):
    list_display = ('fileDataInfoID',
                    'keyword',
                    )
    search_fields = ['keyword']

class personalFileDataAdmin(admin.ModelAdmin):
    list_display = ('ownerAccount',
                    'get_name',
                    'fileDataID',
                    # 'waterMarkPath',
                    'waterCreateReady',
                    'costPoint',
                    'exchangeDate',
                    'expiryDate',
                    )
    search_fields = ['ownerAccount__username','fileDataID__title','ownerAccount__user']
    def get_name(self, obj):
        return obj.ownerAccount.user
    get_name.admin_order_field = 'ownerAccount__user'  # Allows column order sorting
    get_name.short_description = '持有者'  # Renames column head

class personalExchangeFileLogAdmin(admin.ModelAdmin):
    list_display = ('ownerAccount',
                    'get_name',
                    'fileDataID',

                    'exchangeDate',
                    'costPoint',

                    )
    search_fields = ['ownerAccount__username','fileDataID__title','ownerAccount__user']
    list_filter = ('costPoint',)

    def get_name(self, obj):
        return obj.ownerAccount.user
    get_name.admin_order_field = 'ownerAccount__user'  # Allows column order sorting
    get_name.short_description = '持有者'  # Renames column head

admin.site.register(fileDataInfo,fileDataInfoAdmin)
admin.site.register(DBClassInfo,DBClassInfoAdmin)
admin.site.register(secClassInfo)
admin.site.register(fileTypeInfo)
admin.site.register(sourceFromInfo)
admin.site.register(fileDataKeywords,fileDataKeywordsAdmin)
admin.site.register(personalFileData,personalFileDataAdmin)
admin.site.register(personalExchangeFileLog,personalExchangeFileLogAdmin)