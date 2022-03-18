from pdf2image import convert_from_path
from PIL import Image
import os
# ffmpeg -c:v h264_cuvid -i shortTest.mp4 -i  qrcode.png  -filter_complex  "[1:v] scale=120:120 [logo];[0:v][logo]overlay=main_w-overlay_h-15:main_h-overlay_h-15" -c:v h264_nvenc -r 15 -b 500k -y target.mp4

backendCorePath = 'C:/Users/aluo/PycharmProjects/backEndWaterMark/core/'

def create_video_with_waterMark(rawVideoPath,outputVideoPath,qrcodePath,waterMarkPath):

    # 獲取當前檔案路徑，因為我這裡把ffmpeg工具放到了程式碼路徑，所以需要獲取一下當前路徑，這個根據大家實際情況寫
    dir2 = 'C:/Program Files/ImageMagick-7.1.0-Q16-HDRI/ffmpeg.exe'  # ffmpeg具體位置
    # ff = dir + dir  # 組合路徑
    ff = dir2
    result = eval(repr(ff).replace('\\', '/'))
    # 轉換反斜槓為斜槓，因為獲取到的路徑是反斜槓的，需要轉換成斜槓，轉換後會發現是雙斜槓，所以需要下面再轉換下
    ff = result.replace('//', '/')  # 雙斜槓轉為但斜槓
    # cmd = ff + ' -i ' + 'D:\test\abc.flv' + ' -c copy ' + 'D:\test\abc.mp4'
    # 寫需要執行的命令
    # os.system(cmd)  # 執行系統命令，也就是進行轉碼

    dir2 = 'ffmpeg'  # ffmpeg具體位置
        # ff = dir + dir  # 組合路徑
    ff = dir2
    result = eval(repr(ff).replace('\\', '/'))
    # 轉換反斜槓為斜槓，因為獲取到的路徑是反斜槓的，需要轉換成斜槓，轉換後會發現是雙斜槓，所以需要下面再轉換下
    ff = result.replace('//', '/')  # 雙斜槓轉為但斜槓
    # cmd = ff + ' -c:v h264_cuvid -i {rawVideoPath} -i  {qrcodePath} -i {waterMarkPath} -filter_complex  "[1:v] scale=120:120 [logo];[0:v][logo]overlay=main_w-overlay_h-15:main_h-overlay_h-15,overlay=0:0" -c:v h264_nvenc -r 15 -b 500k -y {targetPath}'.format(
    #             rawVideoPath=rawVideoPath,qrcodePath=qrcodePath,waterMarkPath=waterMarkPath,targetPath=outputVideoPath)
    ""
    cmd = ff + ' -i {rawVideoPath} -i  {qrcodePath} -i {waterMarkPath} -c:a aac -c:v h264 -s 1280x720 -b:v 2100000 -maxrate 2100000 -bufsize 2100000  -filter_complex  "[1:v] scale=120:120 [logo];[0:v][logo]overlay=main_w-overlay_h-15:main_h-overlay_h-15,overlay=0:0" -map 0:1 -map 0:0 -map 1:0 -threads 4 -preset ultrafast -c:a  copy -y {targetPath}'.format(
                rawVideoPath=rawVideoPath,qrcodePath=qrcodePath,waterMarkPath=waterMarkPath,targetPath=outputVideoPath)

    print(cmd)
    os.system(cmd)  # 執行系統命令，也就是進行轉碼