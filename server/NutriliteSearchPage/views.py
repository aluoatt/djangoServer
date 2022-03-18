from wsgiref.util import FileWrapper

from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from NutriliteSearchPage.models import fileDataInfo, mainClassInfo, secClassInfo, personalFileData, \
    personalExchangeFileLog, fileDataKeywords,personalWatchFileLog
from userlogin.models import UserAccountInfo, UserAccountChainYenInfo
from NutriliteSearchPage.utils.page import Pagination
import logging
from .tasks import getFileDateProcess, getFileWithoutWaterProcess
import os
import re
import mimetypes
from django.shortcuts import redirect
from django.db.models import Q
import datetime
from dateutil.relativedelta import relativedelta
from django.http.response import StreamingHttpResponse
from pointManage.models import pointHistory
from django.conf import settings
from datetime import timedelta
import numpy as np

backaddress = settings.BACK_ADDRESS


# Create your views here.
def getDimName(value, arg):
    """Removes all values of arg from the given string"""
    return value.filter(amwayNumber=arg).main


# 關鍵字查詢
def keywordSearchPage(request):
    try:
        keywords = request.POST.get("keywords")
        timelim = int(request.POST.get("timelim"))
    except:
        keywords = request.GET.get("keywords")
        timelim = int(request.GET.get("timelim"))

    if keywords is None:
        keywords = ""

    keywords_list = keywords.split(" ")
    mainClass_dict = {}
    for maincls in mainClassInfo.objects.all():
        mainClass_dict[maincls.mainClassName] = maincls.id

    needFilterMainIds = []

    totalKeywordNum = len(keywords_list)

    q1 = Q()
    q1.connector = 'OR'
    fileDataKeywords_list = []

    for keyword in keywords_list:
        if keyword == "":
            totalKeywordNum -= 1
            continue
        if keyword in mainClass_dict.keys():
            needFilterMainIds.append(mainClass_dict[keyword])
            totalKeywordNum -= 1
            continue
        # q1.children.append(("keyword__contains", keyword))
        for fid in np.unique([fileInfo.fileDataInfoID.id for fileInfo in fileDataKeywords.objects.filter(keyword__contains=keyword)]):
            fileDataKeywords_list.append(fid)
    try:
        userAcc = UserAccountInfo.objects.get(username=request.user)
        dataPermissionsLevel = userAcc.dataPermissionsLevel
        userpoint = UserAccountChainYenInfo.objects.get(
            UserAccountInfo=UserAccountInfo.objects.get(username=request.user)).point

    except:
        userpoint = 0
        dataPermissionsLevel = -1
    limDate = (datetime.datetime.now() - relativedelta(years=timelim)).strftime('%Y-%m-%d') + " 23:59:59"

    q2 = Q()
    q2.connector = 'OR'
    earchIdKeywordCount_dict = {}

    fileDataKeywords_obj = fileDataKeywords.objects.filter(q1)

    hasKeywordData = False
    if not keywords == "":
        for keyfileInfo_id in fileDataKeywords_list:
            if keyfileInfo_id in earchIdKeywordCount_dict.keys():
                earchIdKeywordCount_dict[keyfileInfo_id] += 1
                if earchIdKeywordCount_dict[keyfileInfo_id] >= totalKeywordNum:
                    q2.children.append(("id", keyfileInfo_id))
            else:

                earchIdKeywordCount_dict[keyfileInfo_id] = 1
                if earchIdKeywordCount_dict[keyfileInfo_id] >= totalKeywordNum:
                    q2.children.append(("id", keyfileInfo_id))

        titleQ = Q()
        titleQ.connector = "AND"
        for keyword in keywords_list:
            if keyword in mainClass_dict.keys():
                continue
            titleQ.children.append(("title__contains", keyword))

        for titleResult in fileDataInfo.objects.filter(titleQ):
            q2.children.append(("id", titleResult.id))
        clsQ = Q()
        clsQ.connector = "OR"
        for filterMainId in needFilterMainIds:
            clsQ.children.append(("mainClass", filterMainId))

        if len(q2) > 0:
            fileDatas = fileDataInfo.objects.filter(
                occurrenceDate__gte=limDate,
                visible=1,
                permissionsLevel__lte=dataPermissionsLevel
            ).filter(q2 & clsQ).order_by('-occurrenceDate')
        else:
            fileDatas = fileDataInfo.objects.filter(
                occurrenceDate__gte=limDate,
                visible=1,
                permissionsLevel__lte=-1
            )
    else:

        fileDatas = fileDataInfo.objects.filter(
            occurrenceDate__gte=limDate,
            visible=1,
            permissionsLevel__lte=dataPermissionsLevel
        ).order_by('-occurrenceDate')

    if fileDatas.count() > 0:
        hasKeywordData = True

    today = datetime.datetime.now()
    delta = datetime.timedelta(hours=-6)
    target_day = today + delta
    ownFileList = [k.fileDataID.id for k in personalFileData.objects.filter(ownerAccount=userAcc,
                                                                            exchangeDate__gte=target_day)]

    # 總頁數
    page_count = fileDatas.count()
    pageisNotNull = True
    if page_count == 0:
        pageisNotNull = False
    # 當前頁
    current_page_num = request.GET.get("page")
    pagination = Pagination(current_page_num, page_count, request, per_page_num=10, keywords=keywords, timelim=timelim)
    # 處理之後的資料
    fileDatas = fileDatas[pagination.start:pagination.end]

    content = {
        "fileDatas": fileDatas, "pagination": pagination, }

    s = render(request, 'searchPage/KeywordsSearchPage.html', locals())
    s.setdefault('Cache-Control', 'no-store')
    s.setdefault('Expires', 0)
    s.setdefault('Pragma', 'no-cache')
    return s

    # return render(request, 'searchPage/KeywordsSearchPage.html', locals())


# 查詢檔案
def NutriliteSearchPage(request, topic, selectTag):
    selectTag = selectTag
    try:
        userAcc = UserAccountInfo.objects.get(username=request.user)
        dataPermissionsLevel = userAcc.dataPermissionsLevel
        userpoint = UserAccountChainYenInfo.objects.get(
            UserAccountInfo=UserAccountInfo.objects.get(username=request.user)).point

    except:
        userpoint = 0
        dataPermissionsLevel = -1

    if topic == "總部會議":
        topic += "/活動"

    fileDatas = fileDataInfo.objects.filter(mainClass=mainClassInfo.objects.get(mainClassName=topic).id,
                                            secClass=secClassInfo.objects.get(secClassName=selectTag).id,
                                            visible=1,
                                            permissionsLevel__lte=dataPermissionsLevel).order_by('-occurrenceDate')
    today = datetime.datetime.now()
    delta = datetime.timedelta(hours=-6)
    target_day = today + delta
    ownFileList = [k.fileDataID.id for k in personalFileData.objects.filter(ownerAccount=userAcc,
                                                                            exchangeDate__gte=target_day)]

    # 總頁數
    page_count = fileDatas.count()
    pageisNotNull = True
    if page_count == 0:
        pageisNotNull = False
    # 當前頁
    current_page_num = request.GET.get("page")
    pagination = Pagination(current_page_num, page_count, request, per_page_num=10)
    # 處理之後的資料
    fileDatas = fileDatas[pagination.start:pagination.end]

    content = {
        "fileDatas": fileDatas, "pagination": pagination, }
    s = render(request, 'MainSearchPage.html', locals())
    s.setdefault('Cache-Control', 'no-store')
    s.setdefault('Expires', 0)
    s.setdefault('Pragma', 'no-cache')
    return s

def exchangeOption(request, fileId):
    if request.user.has_perm('userlogin.classRoomAccount') and not request.user.is_superuser:
        classRoomAccount = True
    else:
        classRoomAccount = False
    today = datetime.datetime.now()
    delta = datetime.timedelta(hours=-6)
    target_day = today + delta
    targetFile = fileDataInfo.objects.get(id=int(fileId))
    UserAccount = UserAccountInfo.objects.get(username=request.user)
    UserAccountChainYen = UserAccountChainYenInfo.objects.get(UserAccountInfo=UserAccount)
    pf = personalFileData.objects.filter(ownerAccount=UserAccount.id,
                                    fileDataID=targetFile.id)
    alreadyExchange = pf.count() > 0
    if alreadyExchange:
        pf = pf.first()
        if pf.exchangeDate < target_day:

            if targetFile.point > UserAccountChainYen.point:
                targetFile = ""
                return render(request, 'viewFilePage.html', locals())
            else:
                UserAccountChainYen.point = UserAccountChainYen.point - targetFile.point
                UserAccountChainYen.save()
                pHistory = pointHistory(UserAccountInfo=UserAccount, modifier="系統",
                                        recordDate=str(datetime.datetime.now()), reason='兌換資料:' + targetFile.title,
                                        addPoint="", reducePoint=targetFile.point, transferPoint="",
                                        resultPoint=UserAccountChainYen.point)
                pHistory.save()
                targetFile.exchangeCount += 1
                targetFile.save()
                pf.exchangeDate = str(datetime.datetime.now())
                pf.save()

    if request.user == "administrator":
        permission = True
        pointEnough = True
        supervisord = True
    else:
        # 是否兌換

        supervisord = False

        permission = targetFile.permissionsLevel <= UserAccount.dataPermissionsLevel
        # 還沒兌換
        if not alreadyExchange:
            pointEnough = targetFile.point <= UserAccountChainYen.point
        else:
            pointEnough = True

    if (not permission) or (not pointEnough):
        targetFile = ""
        return render(request, 'viewFilePage.html', locals())

    if not supervisord:
        if not alreadyExchange:
            UserAccountChainYen.point = UserAccountChainYen.point - targetFile.point
            UserAccountChainYen.save()

            pHistory = pointHistory(UserAccountInfo=UserAccount, modifier="系統",
                                    recordDate=str(datetime.datetime.now()), reason='兌換資料:' + targetFile.title,
                                    addPoint="", reducePoint=targetFile.point, transferPoint="",
                                    resultPoint=UserAccountChainYen.point)
            pHistory.save()

    if not alreadyExchange:
        personalFileData(fileDataID=targetFile,
                         ownerAccount=UserAccount,
                         expiryDate=None,
                         costPoint=targetFile.point,
                         waterCreateReady=0,
                         create_Date_S=str(datetime.datetime.now()),
                         exchangeDate=str(datetime.datetime.now())
                         ).save()
        targetFile.exchangeCount += 1
        targetFile.save()
        personalExchangeFileLog(fileDataID=targetFile,
                                ownerAccount=UserAccount,
                                costPoint=targetFile.point,

                                ).save()


        if not supervisord:
            waterMarkUserName = UserAccountChainYen.classRoom.ClassRoomCode + "_" + UserAccount.user + "_" \
                                + str(UserAccount.useraccountamwayinfo_set.all().first().amwayNumber)

            # 是否製作浮水印
            if targetFile.downloadAble:
                if targetFile.needWaterMark:

                    if targetFile.fileType.id > 1:  # 非影片
                        # 製作浮水印
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, waterMarkUserName, "pdf",
                                                 UserAccount.id,classRoomAccount)
                    else:
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, waterMarkUserName, "mp4",
                                                 UserAccount.id,classRoomAccount)
                else:
                    if targetFile.fileType.id > 1:  # 非影片
                        getFileWithoutWaterProcess.delay(targetFile.id, targetFile.PDF, waterMarkUserName, "pdf",
                                                         UserAccount.id)
                    else:
                        getFileWithoutWaterProcess.delay(targetFile.id, targetFile.PDF, waterMarkUserName, "mp4",
                                                         UserAccount.id)
            else:
                p = personalFileData.objects.filter(fileDataID=targetFile, ownerAccount=UserAccount).first()
                p.waterCreateReady = 1
                p.waterMarkPath = "cantdownload"
                p.save()
        else:
            if targetFile.downloadAble:
                if targetFile.needWaterMark:


                    if targetFile.fileType.id > 1:  # 非影片
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "pdf", UserAccount.id,classRoomAccount)
                    else:
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "mp4", UserAccount.id,classRoomAccount)
                else:
                    if targetFile.fileType.id > 1:  # 非影片
                        getFileWithoutWaterProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "pdf", UserAccount.id)
                    else:
                        getFileWithoutWaterProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "mp4", UserAccount.id)
            else:
                p = personalFileData.objects.filter(fileDataID=targetFile, ownerAccount=UserAccount).first()
                p.waterCreateReady = 1
                p.waterMarkPath = "cantdownload"
                p.save()
    try:
        persondataInfo = personalFileData.objects.filter(ownerAccount=UserAccount.id,
                                                       fileDataID=targetFile.id).first()
        if persondataInfo.waterCreateReady:
            if os.path.isfile(backaddress + '/'+persondataInfo.waterMarkPath):
                alreadyReady = True


    except:
        alreadyReady = False

    return redirect('/viewFilePage/' + fileId)


###
def regetPersonalFile(request, fileId):
    today = datetime.datetime.now()
    delta = datetime.timedelta(hours=-6)
    target_day = today + delta

    targetFile = fileDataInfo.objects.get(id=int(fileId))
    UserAccount = UserAccountInfo.objects.get(username=request.user)
    alreadyExchange = personalFileData.objects.filter(ownerAccount=UserAccount.id, fileDataID=targetFile.id,
                                                      exchangeDate__gte=target_day).count() > 0

    if request.user.has_perm('userlogin.classRoomAccount') and not request.user.is_superuser:
        classRoomAccount = True
    else:
        classRoomAccount = False

    if request.user == "administrator":
        permission = True
        pointEnough = True
        supervisord = True
    else:
        # 是否兌換

        supervisord = False
        UserAccountChainYen = UserAccountChainYenInfo.objects.get(UserAccountInfo=UserAccount)
        permission = targetFile.permissionsLevel <= UserAccount.dataPermissionsLevel
        # 還沒兌換

        pointEnough = True

    if (not permission) or (not pointEnough):
        targetFile = ""
        return render(request, 'viewFilePage.html', locals())

    if alreadyExchange:

        personalExchangeFileLog(fileDataID=targetFile,
                                ownerAccount=UserAccount,
                                costPoint=-1,
                                ).save()
        if not supervisord:
            waterMarkUserName = UserAccountChainYen.classRoom.ClassRoomCode + "_" + UserAccount.user + "_" \
                                + str(UserAccount.useraccountamwayinfo_set.all().first().amwayNumber)

            # 是否可下載
            if targetFile.downloadAble:
                # 是否製作浮水印
                if targetFile.needWaterMark:
                    if targetFile.fileType.id > 1:  # 非影片
                        # 製作浮水印
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, waterMarkUserName, "pdf",
                                                 UserAccount.id,classRoomAccount)
                    else:
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, waterMarkUserName, "mp4",
                                                 UserAccount.id,classRoomAccount)
                else:
                    if targetFile.fileType.id > 1:  # 非影片
                        # 不製作浮水印
                        getFileWithoutWaterProcess.delay(targetFile.id, targetFile.PDF, waterMarkUserName, "pdf",
                                                         UserAccount.id)
                    else:
                        getFileWithoutWaterProcess.delay(targetFile.id, targetFile.PDF, waterMarkUserName, "mp4",
                                                         UserAccount.id)
            else:
                p = personalFileData.objects.filter(fileDataID=targetFile, ownerAccount=UserAccount).first()
                p.waterCreateReady = 1
                p.waterMarkPath = "cantdownload"
                p.save()
        else:
            if targetFile.downloadAble:
                if targetFile.needWaterMark:
                    if targetFile.fileType.id > 1:  # 非影片
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "pdf", UserAccount.id,classRoomAccount)
                    else:
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "mp4", UserAccount.id,classRoomAccount)
                else:
                    if targetFile.fileType.id > 1:  # 非影片
                        getFileWithoutWaterProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "pdf", UserAccount.id)
                    else:
                        getFileWithoutWaterProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "mp4", UserAccount.id)
            else:
                p = personalFileData.objects.filter(fileDataID=targetFile, ownerAccount=UserAccount).first()
                p.waterCreateReady = 1
                p.waterMarkPath = "cantdownload"
                p.save()
        return True
    else:
        return False


def viewFilePage(request, fileId):
    today = datetime.datetime.now()
    delta = datetime.timedelta(hours=-6)
    target_day = today + delta

    targetFile = fileDataInfo.objects.get(id=int(fileId))
    UserAccount = UserAccountInfo.objects.get(username=request.user)
    personalFile = personalFileData.objects.filter(ownerAccount=UserAccount.id, fileDataID=targetFile.id,
                                                   exchangeDate__gte=target_day)
    alreadyExchange = personalFile.count() > 0
    try:
        pregetStars = personalFile.first().stars
    except:
        pregetStars = 0

    if alreadyExchange:
        aleardyLike = personalFile.first().like
        if ((datetime.datetime.now() - UserAccountInfo.objects.get(username=request.user).last_login) <= timedelta(
                minutes=60 * 5)
                and (datetime.datetime.now() - UserAccountInfo.objects.get(
                    username=request.user).last_login) >= timedelta(
                    minutes=60 * 1)):
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)



    if request.user == "administrator":
        permission = True
        pointEnough = True
        supervisord = True
    else:
        # 是否兌換

        supervisord = False
        UserAccountChainYen = UserAccountChainYenInfo.objects.get(UserAccountInfo=UserAccount)
        permission = targetFile.permissionsLevel <= UserAccount.dataPermissionsLevel
        pointEnough = True
        # 還沒兌換
        if not alreadyExchange:
            return render(request, 'viewFilePage.html', locals())

    #檢查最近一次瀏覽時間
    today = datetime.datetime.now()
    delta = datetime.timedelta(hours=-60)
    target_day = today + delta
    if personalWatchFileLog.objects.filter(watchAccount=UserAccount,exchangeDate__gte=target_day,fileDataID=targetFile).count() < 1:
        personalWatchFileLog(fileDataID=targetFile,
                             watchAccount=UserAccount,
                             exchangeDate=str(datetime.datetime.now())).save()

    try:
        persondataInfo = personalFileData.objects.filter(ownerAccount=UserAccount.id,
                                                         fileDataID=targetFile.id).first()
        if persondataInfo.waterCreateReady:
            if os.path.isfile(backaddress + '/' + persondataInfo.waterMarkPath):
                alreadyReady = True
    except:
        alreadyReady = False

    if (not permission) or (not pointEnough):
        targetFile = ""
        return render(request, 'viewFilePage.html', locals())

    if targetFile.downloadAble:

        s = render(request, 'viewFilePage.html', locals())
    else:
        s = render(request, 'viewFilePageCantDownload.html', locals())
    return s


def returnPDF(request, fileId):
    # Get the applicant's resume
    userAc = UserAccountInfo.objects.get(username=request.user)
    today = datetime.datetime.now()
    delta = datetime.timedelta(hours=-6)
    target_day= today+delta

    resume = personalFileData.objects.filter(fileDataID=fileId, ownerAccount=userAc,exchangeDate__gte=target_day)


    if resume.count() != 1:
        return HttpResponse("error", content_type="text/plain")

    UserAccount = UserAccountInfo.objects.get(username=request.user)

    if UserAccount.dataPermissionsLevel < resume.first().fileDataID.permissionsLevel:
        return HttpResponse("error", content_type="text/plain")

    if resume.first().waterCreateReady == 0:

        if resume.first().create_Date_S < (datetime.datetime.now() - datetime.timedelta(days=1)):

            if regetPersonalFile(request, fileId):

                return HttpResponse("not ready", content_type="text/plain")
            else:
                return HttpResponse("error", content_type="text/plain")
        return HttpResponse("not ready", content_type="text/plain")
    else:

        try:
            if (resume.first().fileDataID.fileType.id == 1):
                return stream_video(request, backaddress + '/' + resume.first().waterMarkPath)
            else:

                response = FileResponse(open(backaddress + '/' + resume.first().waterMarkPath, 'rb'), content_type='application/pdf', filename="pdf.pdf")
        except:
            r = resume.first()
            r.waterCreateReady = False
            r.exchangeDate = str(datetime.datetime.now())
            r.save()
            if regetPersonalFile(request, fileId):

                return HttpResponse("not ready", content_type="text/plain")
            else:
                return HttpResponse("error", content_type="text/plain")
            return HttpResponse("error", content_type="text/plain")

        return response


def returnFileStatus(request, fileId):
    # Get the applicant's resume
    userAc = UserAccountInfo.objects.get(username=request.user)
    today = datetime.datetime.now()
    delta = datetime.timedelta(hours=-6)
    target_day = today + delta
    resume = personalFileData.objects.filter(fileDataID=fileId, ownerAccount=userAc, exchangeDate__gte=target_day)
    if resume.count() != 1:
        return HttpResponse("error", content_type="text/plain")

    UserAccount = UserAccountInfo.objects.get(username=request.user)

    if UserAccount.dataPermissionsLevel < resume.first().fileDataID.permissionsLevel:
        return HttpResponse("error", content_type="text/plain")

    if resume.first().waterCreateReady == 0:

        if resume.first().create_Date_S < (datetime.datetime.now() - datetime.timedelta(days=1)):

            if regetPersonalFile(request, fileId):

                return HttpResponse("not ready", content_type="text/plain")
            else:
                return HttpResponse("error", content_type="text/plain")
        return HttpResponse("not ready", content_type="text/plain")
    else:

        if os.path.isfile(backaddress + '/' + resume.first().waterMarkPath):
            if (resume.first().fileDataID.fileType.id == 1):
                response = HttpResponse("success", content_type="text/plain")
                # return stream_video(request, backaddress + '/' + resume.first().waterMarkPath)
            else:

                fsock = open(backaddress + '/' + resume.first().waterMarkPath, 'rb')

                # response = FileResponse(fsock, content_type='application/pdf', filename="pdf.pdf")
                response = HttpResponse("success", content_type="text/plain")
        else:
            r = resume.first()
            r.waterCreateReady = False
            r.create_Date_S = str(datetime.datetime.now())
            r.save()
            if regetPersonalFile(request, fileId):

                return HttpResponse("not ready", content_type="text/plain")
            else:
                return HttpResponse("error", content_type="text/plain")
            return HttpResponse("error", content_type="text/plain")

        return response

range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


def stream_video(request, path):
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length), status=206,
                                     content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp

#排程
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events,register_job
import time
import os
import traceback
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(),"default")
# @register_job(scheduler,"interval",seconds=3,id="clear_datafile_inVPS_job",replace_existing=True)
@register_job(scheduler,"cron",hour=2,minute=30,id="clear_datafile_inVPS_job",replace_existing=True)
def clear_datafile_inVPS_job():
    for existDatainVPS in personalFileData.objects.filter(waterCreateReady = 1):
        # 1814400
        if os.path.isfile(backaddress + '/' + existDatainVPS.waterMarkPath):
            if (time.time() - os.path.getctime(backaddress+'/'+existDatainVPS.waterMarkPath) ) > 604800: #創建超過21天
                try:
                    os.remove(backaddress+'/'+existDatainVPS.waterMarkPath)
                except:
                    logging.error(traceback.print_exc())

@register_job(scheduler,"cron",hour=1,minute=30,id="auto_backup_db",replace_existing=True)
# @register_job(scheduler,"interval",seconds=10,id="auto_backup_db",replace_existing=True)
def auto_backup_db():
    logging.info("資料庫備份中...  db backup start")
    try:

        os.system('mysqldump -udjangoUser -pchainyen@fmp6u04 djangoserver > {}/djangoserver_info_$(date +%Y%m%d_%H%M%S).sql'.format(dbBackupFolderPath))
    except:
        logging.info("失敗...  db backup start")
    logging.info("資料庫完成中...  db backup finish")

register_events(scheduler)
scheduler.start()

dbBackupFolderPath = '/home/chainyen/production/dbBackup'

