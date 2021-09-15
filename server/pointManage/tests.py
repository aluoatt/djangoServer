from django.test import TestCase
from django.test import Client
from django.contrib.auth.hashers import make_password
from userlogin.models import UserAccountInfo, UserAccountChainYenInfo, chainYenJobTitleInfo, chainYenClassInfo,UserAccountAmwayInfo, registerDDandDimInfo, amwayAwardInfo
from userlogin.models import TempUserAccountInfo, TempUserAccountAmwayInfo, TempUserAccountChainYenInfo

from NutriliteSearchPage.models import sourceFromInfo
# Create your tests here.

class APITestCase(TestCase):
    def setUp(self):
        self.createBasicTable()
        self.createFirstUser()
        self.createSecondUser()
        self.createTestUser()

    def test_point_transfer(self):
        self.c = Client()
        res = self.c.login(username= '20000002000', password = 'a')
        self.assertEqual(res, True)
        res = self.c.post('/pointManage/transferPoint', {'username': '30000003000', 'point':'1'})
        self.assertEqual(res.status_code, 200)
        res = self.c.post('/pointManage/transferPoint', {'username': '30000003000', 'point':'-1'})
        self.assertEqual(res.status_code, 404)
        res = self.c.post('/pointManage/transferPoint', {'username': '30000003000', 'point':'10000000'})
        self.assertEqual(res.status_code, 404)
        res = self.c.post('/pointManage/transferPoint', {'username': '10000001000', 'point':'1'})
        self.assertEqual(res.status_code, 404)

    def createBasicTable(self):
        sourceList = [
            '個人製作',
            '教室製作',
            '總部製作',
            '行動大學',
            'YouTube',
            '公司資料',
            '其他'
        ]
        for sItem in sourceList:
            sourceInfo = sourceFromInfo.objects.filter(sourceFromName = sItem)
            if(not sourceInfo):
                sourceInfo = sourceFromInfo(sourceFromName = sItem)
                sourceInfo.save()

        from NutriliteSearchPage.models import fileTypeInfo
        fileTypeList = [
            '影音檔',
            'PDF',
            'PPT',
            'WORD',
            '圖片/照片',
            '純文字檔',
            '其他'
        ]

        for sItem in fileTypeList:
            fileType = fileTypeInfo.objects.filter(fileTypeName = sItem)
            if(not fileType):
                fileType = fileTypeInfo(fileTypeName = sItem)
                fileType.save()

        from NutriliteSearchPage.models import secClassInfo
        secClassList = [
            '其他',
            '基礎營養',
            '曲線管理',
            '機能性營養',
            '疾病',
            '紐崔萊農場',
            '基礎保養',
            '整體造型',
            '醫美相關',
            '迷思破解',
            '空氣清淨機',
            '淨水器',
            '金鍋',
            '不沾鍋',
            '食譜',
            'Amway Home',
            'G&H',
            'Satinique',
            'Glister',
            'XS 系列',
            '教室課程',
            '基礎會議',
            '菁英會議',
            '老師有約',
            '每月之星',
            '成功領導人',
            '公司創辦人',
            '名人講堂',
            '公司介紹',
            '培訓資料'
        ]
        for data in secClassList:
            secClass = secClassInfo.objects.filter(secClassName=data)
            if(not secClass):
                secClass = secClassInfo.objects.create(secClassName=data)
                secClass.save()

        from NutriliteSearchPage.models import mainClassInfo
        mainClassList = ["營養","美容","科技","金鍋","其他","總部會議/活動","演講廳"]
        for data in mainClassList:
            mainClass = mainClassInfo.objects.filter(mainClassName=data)
            if(not mainClass):
                mainClass = mainClassInfo.objects.create(mainClassName=data)
                mainClass.save()

        from NutriliteSearchPage.models import DBClassInfo
        dbClassList = [
            ['（C）ChainYen專屬（421故事；群雁夥伴個人經歷介紹.....）', "C"],
            ['（A）公司資源（包含安麗公司；YouTube；行動大學；培訓資料.....）', "A"],
            ['（O）其他（包含其他媒體資料.....）', "O"]
        ]
        for data in dbClassList:
            dbClass = DBClassInfo.objects.filter(DBClassName=data[0], DBClassCode=data[1])
            if(not dbClass):
                dbClass = DBClassInfo.objects.create(DBClassName=data[0], DBClassCode=data[1])
                dbClass.save()

        jobList = [
            ['無', 0],
            ['會長', 5],
            ['團長', 10]
        ]

        for data in jobList:
            jobTitle = chainYenJobTitleInfo.objects.filter(jobTitle = data[0])
            if(not jobTitle):
                jobTitle = chainYenJobTitleInfo(jobTitle = data[0], rank=data[1])
                jobTitle.save()

        classRoomList = [
            ['台北', 'CYP', 5],
            ['中壢', 'CYL', 10],
            ['新竹', 'CYS', 15],
            ['台中', 'CYZ', 20],
            ['嘉義', 'CYJ', 25],
            ['永康245', 'CYN1', 30],
            ['永康135', 'CYN2', 35],
            ['良美', 'CYM', 40],
            ['高雄', 'CYK', 45],
            ['屏東', 'CYD', 50],
            ['花蓮', 'CYW', 55],
            ['台東', 'CYT', 60],
            ['澎湖', 'CYH', 65],
            ['海外', 'OVERSEAS', 70],
            ['未進團隊學習', 'None', 75]
        ]
        for data in classRoomList:
            classRoom = chainYenClassInfo.objects.filter(ClassRoomName = data[0])
            if(not classRoom):
                classRoom = chainYenClassInfo(ClassRoomName = data[0], ClassRoomCode=data[1], rank=data[2])
                classRoom.save()


        amAwardList = [
            ['直銷商', 0],
            ['銀獎章', 5],
            ['金獎章', 10],
            ['白金', 15],
            ['創辦人白金', 20],
            ['紅寶石', 25],
            ['創辦人紅寶石', 30],
            ['明珠', 35],
            ['藍寶石', 40],
            ['創辦人藍寶石', 45],
            ['翡翠', 50],
            ['創辦人翡翠', 55],
            ['鑽石', 60],
            ['創辦人鑽石', 65],
            ['執行專才鑽石', 70],
            ['創辦人執行専才鑽石', 75],
            ['雙鑽石', 80],
            ['創辦人雙鑽石', 85],
            ['三鑽石', 90],
            ['創辦人三鑽石', 95],
            ['皇冠', 100],
            ['創辦人皇冠', 105],
            ['皇冠大使', 110],
            ['創辦人皇冠大使', 115]
        ]

        for data in amAwardList:
            amAward = amwayAwardInfo.objects.filter(amwayAward = data[0])
            if(not amAward):
                amAward = amwayAwardInfo(amwayAward = data[0], rank = data[1])
                amAward.save()

    def createFirstUser(self):
        amAward = amwayAwardInfo.objects.get(amwayAward = "創辦人皇冠大使")
        ddInfo = registerDDandDimInfo.objects.filter(amwayNumber = "3003694")
        if not ddInfo:
            ddInfo = registerDDandDimInfo(amwayAward=amAward, amwayNumber="3003694", amwayDiamond="3003694", main = "鍾老師")
            ddInfo.save()
        else:
            ddInfo = ddInfo.first()

        amAward = amwayAwardInfo.objects.get(amwayAward = "鑽石")

        # 將測試使用者註冊註冊新的鑽石編號
        ddInfo = registerDDandDimInfo.objects.filter(amwayNumber = "1000000")
        if not ddInfo:
            ddInfo = registerDDandDimInfo(amwayAward=amAward, amwayNumber="1000000", amwayDiamond="3003694", main = "我是鑽石")
            ddInfo.save()
        else:
            ddInfo = ddInfo.first()

        #將自己的上手領導人設定為鍾老師
        ddInfo = registerDDandDimInfo.objects.get(amwayNumber = "3003694")

        amwayNumber="1000000"
        user = "我是鑽石"
        username = "10000001000"
        classInfo = chainYenClassInfo.objects.get(ClassRoomName = "台北")
        amAward = amwayAwardInfo.objects.get(amwayAward = "鑽石")
        jobTitle = chainYenJobTitleInfo.objects.get(jobTitle = "會長")
        is_superuser=1
        self.createUser(amwayNumber, amAward, ddInfo, user, username, jobTitle, classInfo, is_superuser)

    def createSecondUser(self):
        amAward = amwayAwardInfo.objects.get(amwayAward = "鑽石")

        # 將測試使用者註冊註冊新的白金編號
        ddInfo = registerDDandDimInfo.objects.filter(amwayNumber = "2000000")
        if not ddInfo:
            ddInfo = registerDDandDimInfo(amwayAward=amAward, amwayNumber="2000000", amwayDiamond="1000000", main = "我是白金")
            ddInfo.save()
        else:
            ddInfo = ddInfo.first()

        #將自己的上手領導人設定為我是鑽石
        ddInfo = registerDDandDimInfo.objects.get(amwayNumber = "1000000")

        amwayNumber="2000000"
        user = "我是白金"
        username = "20000002000"
        classInfo = chainYenClassInfo.objects.get(ClassRoomName = "台北")
        amAward = amwayAwardInfo.objects.get(amwayAward = "白金")
        jobTitle = chainYenJobTitleInfo.objects.get(jobTitle = "無")
        is_superuser=0
        self.createUser(amwayNumber, amAward, ddInfo, user, username, jobTitle, classInfo, is_superuser)

    def createTestUser(self):
        # 指定給白金
        DDNumber = "2000000"
        for i in range(3):
            user = "我的 DD 是白金" + str(i)
            amwayNumber = str(3000000)
            IDNumber = str(3000 + i)
            username = amwayNumber + IDNumber
            jobTitle = chainYenJobTitleInfo.objects.get(jobTitle = "無")
            classInfo = chainYenClassInfo.objects.get(ClassRoomName = "台北")
            amAward = amwayAwardInfo.objects.get(amwayAward = "直銷商")
            ddInfo = registerDDandDimInfo.objects.get(amwayNumber = DDNumber)
            is_superuser=0
            self.createUser(amwayNumber, amAward, ddInfo, user, username, jobTitle, classInfo, is_superuser)
    
    def createUser(self, amwayNumber, amAward, ddInfo, user, 
                    username, jobTitle, classInfo, is_superuser):
        if UserAccountInfo.objects.filter(username = username):
            return
        r = UserAccountInfo(username = username,
            user=user,
            gender="男",
            phone="000000000",
            password=make_password("a"),
            is_superuser=is_superuser,
            is_staff=1,
            is_active=1,
            dataPermissionsLevel=99,
            email="123@gmail.com")
        r2 = UserAccountChainYenInfo(UserAccountInfo=r,
            jobTitle=jobTitle,
            classRoom=classInfo,
            accountStatus="正常",
            freezeDate=None,
            point=10000,
            EM=False)

        r3 = UserAccountAmwayInfo(UserAccountInfo=r,
            amwayNumber=amwayNumber,
            amwayAward=amAward,
            amwayDD=ddInfo)
        r.save()
        r2.save()
        r3.save()
