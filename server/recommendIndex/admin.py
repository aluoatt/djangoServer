from django.contrib import admin

# Register your models here.
from django.contrib import admin
from recommendIndex.models import recommendIndexInfo

class recommendIndexInfoAdmin(admin.ModelAdmin):
    list_display = ('mainClass',
                    'keywords',

                    )
    search_fields = ['mainClass__mainClassName']
    list_filter = ('mainClass',)

admin.site.register(recommendIndexInfo,recommendIndexInfoAdmin)