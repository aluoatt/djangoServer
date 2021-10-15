from django.contrib.auth.models import Group, Permission

seeManagerArticlePage = Permission.objects.get(name = "seeManagerArticlePage")
seeManagerArticleReportPage = Permission.objects.get(name = "seeManagerArticleReportPage")
articlePointManage = Permission.objects.get(name = "articlePointManage")



ArtistryArticleManage = Permission.objects.get(name = "ArtistryArticleManage")
artistryArticleManager, created = Group.objects.get_or_create(name='美容組資料管理者')
if created:
    artistryArticleManager.permissions.add(ArtistryArticleManage)
    artistryArticleManager.permissions.add(seeManagerArticlePage)
    artistryArticleManager.permissions.add(seeManagerArticleReportPage)

NutrilliteArticleManage = Permission.objects.get(name = "NutrilliteArticleManage")
nutrilliteArticleManager, created = Group.objects.get_or_create(name='營養組資料管理者')
if created:
    nutrilliteArticleManager.permissions.add(seeManagerArticlePage)
    nutrilliteArticleManager.permissions.add(NutrilliteArticleManage)
    nutrilliteArticleManager.permissions.add(seeManagerArticleReportPage)

TechArticleManage = Permission.objects.get(name = "TechArticleManage")
techArticleManager, created = Group.objects.get_or_create(name='科技組資料管理者')
if created:
    techArticleManager.permissions.add(seeManagerArticlePage)
    techArticleManager.permissions.add(TechArticleManage)
    techArticleManager.permissions.add(seeManagerArticleReportPage)

AmwayQueenArticleManage = Permission.objects.get(name = "AmwayQueenArticleManage")
amwayQueenArticleManager, created = Group.objects.get_or_create(name='金鍋組資料管理者')
if created:
    amwayQueenArticleManager.permissions.add(seeManagerArticlePage)
    amwayQueenArticleManager.permissions.add(AmwayQueenArticleManage)
    amwayQueenArticleManager.permissions.add(seeManagerArticleReportPage)

OtherArticleManage = Permission.objects.get(name = "OtherArticleManage")
otherArticleManager, created = Group.objects.get_or_create(name='其他組資料管理者')
if created:
    otherArticleManager.permissions.add(seeManagerArticlePage)
    otherArticleManager.permissions.add(OtherArticleManage)
    otherArticleManager.permissions.add(seeManagerArticleReportPage)

ChainyenArticleManage = Permission.objects.get(name = "ChainyenArticleManage")
chainyenArticleManager, created = Group.objects.get_or_create(name='群雁總部資料管理者')
if created:
    chainyenArticleManager.permissions.add(seeManagerArticlePage)
    chainyenArticleManager.permissions.add(ChainyenArticleManage)
    chainyenArticleManager.permissions.add(seeManagerArticleReportPage)

SpeechArticleManage = Permission.objects.get(name = "SpeechArticleManage")
speechArticleManager, created = Group.objects.get_or_create(name='演講廳資料管理者')
if created:
    speechArticleManager.permissions.add(seeManagerArticlePage)
    speechArticleManager.permissions.add(SpeechArticleManage)
    speechArticleManager.permissions.add(seeManagerArticleReportPage)


# 文章管理大人
articleAdminManager, created = Group.objects.get_or_create(name='資料超級管理者')
if created:
    articleAdminManager.permissions.add(seeManagerArticlePage)
    articleAdminManager.permissions.add(articlePointManage)
    articleAdminManager.permissions.add(ArtistryArticleManage)
    articleAdminManager.permissions.add(NutrilliteArticleManage)
    articleAdminManager.permissions.add(TechArticleManage)
    articleAdminManager.permissions.add(AmwayQueenArticleManage)
    articleAdminManager.permissions.add(OtherArticleManage)
    articleAdminManager.permissions.add(ChainyenArticleManage)
    articleAdminManager.permissions.add(SpeechArticleManage)

#可以回報文章問題
articleReport = Permission.objects.get(name = "articleReport")
articleReporter, created = Group.objects.get_or_create(name='文章回報組')
articleReporter.permissions.add(articleReport)
