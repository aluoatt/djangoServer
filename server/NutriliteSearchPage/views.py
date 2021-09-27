from wsgiref.util import FileWrapper

from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from NutriliteSearchPage.models import fileDataInfo, mainClassInfo, secClassInfo, personalFileData, \
    personalExchangeFileLog, fileDataKeywords
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

backaddress = "/home/chainyen/production/backEnd"


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
    totalKeywordNum = len(keywords_list)

    q1 = Q()
    q1.connector = 'OR'

    for keyword in keywords_list:
        q1.children.append(("keyword__contains", keyword))

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
        for keyfileInfo in fileDataKeywords_obj:
            if keyfileInfo.fileDataInfoID.id in earchIdKeywordCount_dict.keys():
                earchIdKeywordCount_dict[keyfileInfo.fileDataInfoID.id] += 1
                if earchIdKeywordCount_dict[keyfileInfo.fileDataInfoID.id] >= totalKeywordNum:
                    q2.children.append(("id", keyfileInfo.fileDataInfoID.id))
            else:

                earchIdKeywordCount_dict[keyfileInfo.fileDataInfoID.id] = 1
                if earchIdKeywordCount_dict[keyfileInfo.fileDataInfoID.id] >= totalKeywordNum:
                    q2.children.append(("id", keyfileInfo.fileDataInfoID.id))

        titleQ = Q()
        titleQ.connector = "AND"
        for keyword in keywords_list:
            titleQ.children.append(("title__contains", keyword))

        for titleResult in fileDataInfo.objects.filter(titleQ):
            q2.children.append(("id", titleResult.id))


        if len(q2) > 0:
            fileDatas = fileDataInfo.objects.filter(
                occurrenceDate__gte=limDate,
                visible=1,
                permissionsLevel__lte=dataPermissionsLevel
            ).filter(q2).order_by('occurrenceDate')
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
        ).order_by('occurrenceDate')

    if fileDatas.count() > 0:
        hasKeywordData = True

    ownFileList = [k.fileDataID.id for k in personalFileData.objects.filter(ownerAccount=userAcc)]

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
                                            permissionsLevel__lte=dataPermissionsLevel).order_by('occurrenceDate')

    ownFileList = [k.fileDataID.id for k in personalFileData.objects.filter(ownerAccount=userAcc)]

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
    targetFile = fileDataInfo.objects.get(id=int(fileId))
    UserAccount = UserAccountInfo.objects.get(username=request.user)
    alreadyExchange = personalFileData.objects.filter(ownerAccount=UserAccount.id, fileDataID=targetFile.id).count() > 0

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
                                    recordDate=datetime.datetime.now(), reason='兌換資料',
                                    addPoint="", reducePoint=targetFile.point, transferPoint="",
                                    resultPoint=UserAccountChainYen.point)
            pHistory.save()

    if not alreadyExchange:
        personalFileData(fileDataID=targetFile,
                         ownerAccount=UserAccount,
                         expiryDate=None,
                         costPoint=targetFile.point,
                         waterCreateReady=0,
                         exchangeDate=datetime.datetime.now()
                         ).save()

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
                                                 UserAccount.id)
                    else:
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, waterMarkUserName, "mp4",
                                                 UserAccount.id)
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
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "pdf", UserAccount.id)
                    else:
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "mp4", UserAccount.id)
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
    return redirect('/viewFilePage/' + fileId)


###
def regetPersonalFile(request, fileId):
    targetFile = fileDataInfo.objects.get(id=int(fileId))
    UserAccount = UserAccountInfo.objects.get(username=request.user)
    alreadyExchange = personalFileData.objects.filter(ownerAccount=UserAccount.id, fileDataID=targetFile.id).count() > 0

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
                                                 UserAccount.id)
                    else:
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, waterMarkUserName, "mp4",
                                                 UserAccount.id)
                else:
                    if targetFile.fileType.id > 1:  # 非影片
                        # 製作浮水印
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
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "pdf", UserAccount.id)
                    else:
                        getFileDateProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "mp4", UserAccount.id)
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
    targetFile = fileDataInfo.objects.get(id=int(fileId))
    UserAccount = UserAccountInfo.objects.get(username=request.user)
    personalFile = personalFileData.objects.filter(ownerAccount=UserAccount.id, fileDataID=targetFile.id)
    alreadyExchange = personalFile.count() > 0
    if alreadyExchange:
        aleardyLike = personalFile.first().like
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
        #     pointEnough = targetFile.point <= UserAccountChainYen.point
        # else:
        #     pointEnough = True

    if (not permission) or (not pointEnough):
        targetFile = ""
        return render(request, 'viewFilePage.html', locals())

    if targetFile.downloadAble:

        s = render(request, 'viewFilePage.html', locals())
        # s.setdefault('Cache-Control', 'no-store')
        # s.setdefault('Expires', 0)
        # s.setdefault('Pragma', 'no-cache')
        # return render(request, 'viewFilePage.html', locals())


    else:
        s = render(request, 'viewFilePageCantDownload.html', locals())
        # s.setdefault('Cache-Control', 'no-store')
        # s.setdefault('Expires', 0)
        # s.setdefault('Pragma', 'no-cache')
    return s


def returnPDF(request, fileId):
    # Get the applicant's resume
    userAc = UserAccountInfo.objects.get(username=request.user)
    resume = personalFileData.objects.filter(fileDataID=fileId, ownerAccount=userAc)

    if resume.count() != 1:
        return HttpResponse("error", content_type="text/plain")

    UserAccount = UserAccountInfo.objects.get(username=request.user)

    if UserAccount.dataPermissionsLevel < resume.first().fileDataID.permissionsLevel:
        return HttpResponse("error", content_type="text/plain")

    if resume.first().waterCreateReady == 0:

        if resume.first().exchangeDate < (datetime.datetime.now() - datetime.timedelta(days=1)):

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

                # fsock = open(backaddress + '/' + resume.first().waterMarkPath, 'rb')

                response = FileResponse(open(backaddress + '/' + resume.first().waterMarkPath, 'rb'), content_type='application/pdf', filename="pdf.pdf")
        except:
            r = resume.first()
            r.waterCreateReady = False
            r.exchangeDate = datetime.datetime.now()
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
    resume = personalFileData.objects.filter(fileDataID=fileId, ownerAccount=userAc)

    if resume.count() != 1:
        return HttpResponse("error", content_type="text/plain")

    UserAccount = UserAccountInfo.objects.get(username=request.user)

    if UserAccount.dataPermissionsLevel < resume.first().fileDataID.permissionsLevel:
        return HttpResponse("error", content_type="text/plain")

    if resume.first().waterCreateReady == 0:

        if resume.first().exchangeDate < (datetime.datetime.now() - datetime.timedelta(days=1)):

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
            r.exchangeDate = datetime.datetime.now()
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
            if (time.time() - os.path.getctime(backaddress+'/'+existDatainVPS.waterMarkPath) ) > 1814400: #創建超過21天
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

