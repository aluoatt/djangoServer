from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from wsgiref.util import FileWrapper
import os
import re
import mimetypes
from django.conf import settings
import logging
from django.http import HttpResponse, FileResponse
from .models import replayVideoInfo
from datetime import datetime, timedelta
import json
from io import StringIO

backaddress = settings.BACK_ADDRESS

def index(request):
    currentDate = datetime.now().replace(minute=0, hour=0, second=0, microsecond=0)
    weekDay = currentDate.weekday()
    weekstart = currentDate - timedelta(days=(weekDay))
    weekEnd   = weekstart + timedelta(days=5)
    videoInfos = replayVideoInfo.objects.filter(recordDate__range=[weekstart, weekEnd])
    weekVideo = {}
    for data in videoInfos:
        if data.classRoom not in weekVideo:
            weekVideo[data.classRoom] = []
            for i in range(5):
                weekVideo[data.classRoom].append("")
        weekVideo[data.classRoom][data.recordDate.weekday()] = {
            "title": data.title,
            "classRoom": data.classRoom,
            "recordDate": str(data.recordDate),
            "id": data.id
        }
    weekVideo = json.dumps(weekVideo)
    return render(request, 'courseReplay/index.html', locals())

def viewFilePage(request, fileId):
    targetFile = replayVideoInfo.objects.get(id = fileId)
    return render(request, 'courseReplay/viewFilePage.html', locals())

def returnVideo(request, fileId):
    try:
        videoInfo = replayVideoInfo.objects.get(id = fileId)
        return stream_video(request, backaddress + '/coursereplay/' + videoInfo.title + ".mp4")
    except:
        r = replayVideoInfo.objects.get(id = fileId)
        r.waterCreateReady = False
        r.exchangeDate = str(datetime.datetime.now())
        r.save()
        return HttpResponse("not ready", content_type="text/plain")

def returnFileStatus(request, fileId):
    videoInfo = replayVideoInfo.objects.filter(id = fileId).get()
    
    if os.path.isfile(backaddress + '/coursereplay/' + videoInfo.title + ".mp4"):
        if videoInfo.recordDate < datetime.now().replace(minute=0, hour=0, second=0, microsecond=0):
            response = HttpResponse("not ready", content_type="text/plain")
        else:
            response = HttpResponse("success", content_type="text/plain")
    else:
        response = HttpResponse("not ready", content_type="text/plain")

    return response

def confirmViewFileSubmit(request):
    return HttpResponse("OK", content_type="text/plain")

def webvtt(request):
    x = """WEBVTT

            00:00:00.000 --> 00:10:07.080 align:left line:50%
            CYP_吳念組_9811721 CYP_吳念組_9811721 

            00:00:00.000 --> 00:10:07.080 align:left line:0%
            CYP_吳念組_9811721 CYP_吳念組_9811721 

            00:00:00.000 --> 00:10:07.080 align:middle line:90%
            僅供內部使用, 請勿外流!
            """
    return HttpResponse(x, content_type="text/plain")

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
import requests
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(),"default")
# @register_job(scheduler,"interval",seconds=3,id="clear_datafile_inVPS_job",replace_existing=True)

#@register_job(scheduler,"interval",seconds=180000,id="sync_replay_data_job",replace_existing=True)
@register_job(scheduler,"cron",hour=1,minute=30,id="sync_replay_data_job",replace_existing=True)
def sync_replay_data_job():
    try:
        currentDate = datetime.now()
        weekDay = currentDate.weekday()
        weekstart = currentDate - timedelta(days=(weekDay-1))
        weekEnd   = weekstart + timedelta(days=4)
        videoInfos = replayVideoInfo.objects.filter(recordDate__range=[weekstart, weekEnd])
        weekVideo = []
        for data in videoInfos:
            weekVideo.append({
                "name":data.title,
                "fileid":data.fileid
            })
        r = requests.post('http://127.0.0.1:9104/v1/syncReplayVideo', data=json.dumps(weekVideo)).text
    except Exception as e:
        pass

@register_job(scheduler,"interval",seconds=10,id="sync_replay_info_job",replace_existing=True)
#@register_job(scheduler,"cron",hour=1,minute=30,id="sync_replay_info_job",replace_existing=True)
def sync_replay_info_job():
    try:
        r = requests.get('http://127.0.0.1:9104/v1/getReplayList').text
        r = json.loads(r)
        for itme in r:
            filename = itme['name']
            try:
                recordDate = datetime.strptime(filename.split("_")[0], "%Y.%m.%d")
                classRoom = filename.split("_")[1]
                fileid = itme['fileid']
                if not replayVideoInfo.objects.filter(title=filename, recordDate=recordDate,
                    classRoom=classRoom,fileid =fileid):
                    replayVideoInfo(title = filename, recordDate=recordDate, 
                        classRoom=classRoom, fileid = fileid).save()
            except Exception as e:
                pass
    except Exception as e:
        pass
register_events(scheduler)
scheduler.start()
