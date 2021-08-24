from wsgiref.util import FileWrapper

from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from NutriliteSearchPage.models import fileDataInfo,mainClassInfo,secClassInfo,personalFileData,personalExchangeFileLog
from userlogin.models import UserAccountInfo,UserAccountChainYenInfo
from NutriliteSearchPage.utils.page import Pagination
import logging
from .tasks import getFileDateProcess
import os
import re
import mimetypes
from django.shortcuts import redirect

from django.http.response import StreamingHttpResponse
backaddress = "/home/aluo/backEnd"
# Create your views here.
# 查詢檔案
def NutriliteSearchPage(request,topic,selectTag):
    selectTag = selectTag
    try:
        dataPermissionsLevel = UserAccountInfo.objects.get(username=request.user).dataPermissionsLevel
        userpoint = UserAccountChainYenInfo.objects.get(UserAccountInfo=UserAccountInfo.objects.get(username=request.user)).point

    except:
        userpoint = 0
        dataPermissionsLevel = -1

    if topic == "總部會議":
        topic += "/活動"

    fileDatas = fileDataInfo.objects.filter(mainClass = mainClassInfo.objects.get(mainClassName=topic).id,
                                           secClass = secClassInfo.objects.get(secClassName=selectTag).id,
                                           visible = 1,
                                           permissionsLevel__lte = dataPermissionsLevel).order_by('occurrenceDate')
    # 總頁數
    page_count = fileDatas.count()
    pageisNotNull = True
    if page_count == 0:
        pageisNotNull = False
    # 當前頁
    current_page_num = request.GET.get("page")
    pagination = Pagination(current_page_num, page_count,request, per_page_num=10)
    # 處理之後的資料
    fileDatas = fileDatas[pagination.start:pagination.end]

    content = {
        "fileDatas": fileDatas, "pagination": pagination, }

    return render(request, 'MainSearchPage.html', locals())

def exchangeOption(request,fileId):
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
    if not alreadyExchange:
        personalFileData(fileDataID=targetFile,
                         ownerAccount=UserAccount,
                         expiryDate=None,
                         costPoint=targetFile.point,
                         waterCreateReady=0,
                         ).save()

        personalExchangeFileLog(fileDataID=targetFile,
                                ownerAccount=UserAccount,
                                costPoint=targetFile.point,
                                ).save()
        if not supervisord:
            waterMarkUserName = UserAccountChainYen.classRoom.ClassRoomCode + "_" + UserAccount.user + "_" \
                                + str(UserAccount.useraccountamwayinfo_set.all().first().amwayNumber)
            if targetFile.fileType.id > 1:  # 非影片
                # 製作浮水印
                getFileDateProcess.delay(targetFile.id, targetFile.PDF, waterMarkUserName, "pdf", UserAccount.id)
            else:
                getFileDateProcess.delay(targetFile.id, targetFile.file, waterMarkUserName, "mp4", UserAccount.id)
        else:
            if targetFile.fileType.id > 1:  # 非影片
                getFileDateProcess.delay(targetFile.id, targetFile.PDF, "超級使用者", "pdf", UserAccount.id)
            else:
                getFileDateProcess.delay(targetFile.id, targetFile.file, "超級使用者", "mp4", UserAccount.id)
    # 發請求
    # s = render(request, 'viewFilePage.html', locals())
    # s.setdefault('Cache-Control', 'no-store')
    # s.setdefault('Expires', 0)
    # s.setdefault('Pragma', 'no-cache')
    # return render(request, 'viewFilePage.html', locals())

    return redirect('/viewFilePage/'+fileId)

def viewFilePage(request,fileId):
    
    targetFile = fileDataInfo.objects.get(id=int(fileId))
    UserAccount = UserAccountInfo.objects.get(username=request.user)
    alreadyExchange = personalFileData.objects.filter(ownerAccount=UserAccount.id,fileDataID=targetFile.id).count() > 0

    if request.user == "administrator":
        permission = True
        pointEnough = True
        supervisord = True
    else:
        #是否兌換

        supervisord = False
        UserAccountChainYen = UserAccountChainYenInfo.objects.get(UserAccountInfo=UserAccount)
        permission = targetFile.permissionsLevel <= UserAccount.dataPermissionsLevel
        pointEnough = True
        #還沒兌換
        if not alreadyExchange:
            return render(request, 'viewFilePage.html', locals())
        #     pointEnough = targetFile.point <= UserAccountChainYen.point
        # else:
        #     pointEnough = True

    if (not permission) or (not pointEnough):
        targetFile = ""
        return render(request, 'viewFilePage.html', locals())

    # if not supervisord:
    #     if not aleardyExchange:
    #         UserAccountChainYen.point = UserAccountChainYen.point - targetFile.point
    #         UserAccountChainYen.save()
    # if not aleardyExchange:
    #     personalFileData(fileDataID=targetFile,
    #                      ownerAccount=UserAccount,
    #                      expiryDate=None,
    #                      costPoint=targetFile.point,
    #                      waterCreateReady=0,
    #                      ).save()
    #
    #     personalExchangeFileLog(fileDataID=targetFile,
    #                             ownerAccount=UserAccount,
    #                             costPoint=targetFile.point,
    #                             ).save()
    #     if not supervisord:
    #         waterMarkUserName = UserAccountChainYen.classRoom.ClassRoomCode + "_" + UserAccount.user + "_"  \
    #                             + str(UserAccount.useraccountamwayinfo_set.all().first().amwayNumber)
    #         if targetFile.fileType.id > 1:# 非影片
    #             #製作浮水印
    #             getFileDateProcess.delay(targetFile.id,targetFile.PDF,waterMarkUserName,"pdf",UserAccount.id)
    #         else:
    #             getFileDateProcess.delay(targetFile.id,targetFile.file,waterMarkUserName, "mp4",UserAccount.id)
    #     else:
    #         if targetFile.fileType.id > 1:  # 非影片
    #             getFileDateProcess.delay(targetFile.id,targetFile.PDF,"超級使用者", "pdf",UserAccount.id)
    #         else:
    #             getFileDateProcess.delay(targetFile.id,targetFile.file,"超級使用者", "mp4",UserAccount.id)
    # 發請求
    s = render(request, 'viewFilePage.html', locals())
    s.setdefault('Cache-Control', 'no-store')
    s.setdefault('Expires', 0)
    s.setdefault('Pragma', 'no-cache')
    # return render(request, 'viewFilePage.html', locals())

    return s

def returnPDF(request, fileId):
    # Get the applicant's resume
    userAc = UserAccountInfo.objects.get(username=request.user)
    resume = personalFileData.objects.filter(fileDataID=fileId,ownerAccount=userAc)
    if resume.count() != 1:
        return HttpResponse("error", content_type="text/plain")

    UserAccount = UserAccountInfo.objects.get(username=request.user)

    if UserAccount.dataPermissionsLevel < resume.first().fileDataID.permissionsLevel:
        return HttpResponse("error", content_type="text/plain")

    if resume.first().waterCreateReady == 0:
        return HttpResponse("not ready", content_type="text/plain")

    if (resume.first().fileDataID.fileType.id ==1 ):
        # file = FileWrapper(open(backaddress+'/'+resume.first().waterMarkPath, 'rb'))
        # response = HttpResponse(file, content_type='video/mp4')
        # response['Content-Disposition'] = 'attachment; filename=my_video.mp4'
        return stream_video(request,backaddress+'/'+resume.first().waterMarkPath)
    else:
        fsock = open(backaddress + '/' + resume.first().waterMarkPath, 'rb')
        response = FileResponse(fsock, content_type='application/pdf', filename="pdf.pdf")

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
        resp = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp