from django.db import models

# Create your models here.

class recommendIndexInfo(models.Model):
    mainClass = models.ForeignKey("NutriliteSearchPage.mainClassInfo", verbose_name='主類別', on_delete=models.PROTECT)
    keywords = models.CharField(max_length=40, verbose_name='關鍵字名稱')
    class Meta:
        verbose_name = "關鍵字推薦索引設定"
        verbose_name_plural = "關鍵字推薦索引設定"

    def __str__(self):
        return self.keywords