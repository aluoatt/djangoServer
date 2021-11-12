from django.contrib.auth.models import Group, Permission

articleReport = Permission.objects.get(codename = "articleReport")
seeManagerArticlePage = Permission.objects.get(codename = "seeManagerArticlePage")
seeManagerArticleReportPage = Permission.objects.get(codename = "seeManagerArticleReportPage")
articlePointManage = Permission.objects.get(codename = "articlePointManage")
seeManagerMenuButton = Permission.objects.get(codename = "seeManagerMenuButton")



ArtistryArticleManage = Permission.objects.get(codename = "ArtistryArticleManage")
artistryArticleManager, created = Group.objects.get_or_create(name='美容組資料管理者')
if created:
    artistryArticleManager.permissions.add(ArtistryArticleManage)
    artistryArticleManager.permissions.add(seeManagerArticlePage)
    artistryArticleManager.permissions.add(seeManagerArticleReportPage)
    artistryArticleManager.permissions.add(seeManagerMenuButton)

NutrilliteArticleManage = Permission.objects.get(codename = "NutrilliteArticleManage")
nutrilliteArticleManager, created = Group.objects.get_or_create(name='營養組資料管理者')
if created:
    nutrilliteArticleManager.permissions.add(seeManagerArticlePage)
    nutrilliteArticleManager.permissions.add(NutrilliteArticleManage)
    nutrilliteArticleManager.permissions.add(seeManagerArticleReportPage)
    nutrilliteArticleManager.permissions.add(seeManagerMenuButton)

TechArticleManage = Permission.objects.get(codename = "TechArticleManage")
techArticleManager, created = Group.objects.get_or_create(name='科技組資料管理者')
if created:
    techArticleManager.permissions.add(seeManagerArticlePage)
    techArticleManager.permissions.add(TechArticleManage)
    techArticleManager.permissions.add(seeManagerArticleReportPage)
    techArticleManager.permissions.add(seeManagerMenuButton)

AmwayQueenArticleManage = Permission.objects.get(codename = "AmwayQueenArticleManage")
amwayQueenArticleManager, created = Group.objects.get_or_create(name='金鍋組資料管理者')
if created:
    amwayQueenArticleManager.permissions.add(seeManagerArticlePage)
    amwayQueenArticleManager.permissions.add(AmwayQueenArticleManage)
    amwayQueenArticleManager.permissions.add(seeManagerArticleReportPage)
    amwayQueenArticleManager.permissions.add(seeManagerMenuButton)

OtherArticleManage = Permission.objects.get(codename = "OtherArticleManage")
otherArticleManager, created = Group.objects.get_or_create(name='其他組資料管理者')
if created:
    otherArticleManager.permissions.add(seeManagerArticlePage)
    otherArticleManager.permissions.add(OtherArticleManage)
    otherArticleManager.permissions.add(seeManagerArticleReportPage)
    otherArticleManager.permissions.add(seeManagerMenuButton)

ChainyenArticleManage = Permission.objects.get(codename = "ChainyenArticleManage")
chainyenArticleManager, created = Group.objects.get_or_create(name='群雁總部資料管理者')
if created:
    chainyenArticleManager.permissions.add(seeManagerArticlePage)
    chainyenArticleManager.permissions.add(ChainyenArticleManage)
    chainyenArticleManager.permissions.add(seeManagerArticleReportPage)
    chainyenArticleManager.permissions.add(seeManagerMenuButton)

SpeechArticleManage = Permission.objects.get(codename = "SpeechArticleManage")
speechArticleManager, created = Group.objects.get_or_create(name='演講廳資料管理者')
if created:
    speechArticleManager.permissions.add(seeManagerArticlePage)
    speechArticleManager.permissions.add(SpeechArticleManage)
    speechArticleManager.permissions.add(seeManagerArticleReportPage)
    speechArticleManager.permissions.add(seeManagerMenuButton)


# 文章管理大人
articleAdminManager, created = Group.objects.get_or_create(name='資料超級管理者')
if created:
    articleAdminManager.permissions.add(seeManagerArticlePage)
    articleAdminManager.permissions.add(seeManagerArticleReportPage)
    articleAdminManager.permissions.add(articlePointManage)
    articleAdminManager.permissions.add(ArtistryArticleManage)
    articleAdminManager.permissions.add(NutrilliteArticleManage)
    articleAdminManager.permissions.add(TechArticleManage)
    articleAdminManager.permissions.add(AmwayQueenArticleManage)
    articleAdminManager.permissions.add(OtherArticleManage)
    articleAdminManager.permissions.add(ChainyenArticleManage)
    articleAdminManager.permissions.add(SpeechArticleManage)
    articleAdminManager.permissions.add(articleReport)
    articleAdminManager.permissions.add(seeManagerMenuButton)

#可以回報文章問題
articleReporter, created = Group.objects.get_or_create(name='文章回報組')
articleReporter.permissions.add(articleReport)
