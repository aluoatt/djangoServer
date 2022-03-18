import getpass
import subprocess

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdf2image import convert_from_path
pdfmetrics.registerFont(TTFont('NotoSansCJKtc-Medium', './core/SourceHanSansTC-Regular.ttf'))
# pdfmetrics.registerFont(TTFont('NotoSansCJKtc-Medium', './SourceHanSansTC-Regular.ttf'))
from PyPDF2 import PdfFileWriter, PdfFileReader
from core.creatQRCode import createQR
# from creatQRCode import createQR
import datetime
import os
from core.videoAddWaterMark import create_video_with_waterMark
# from videoAddWaterMark import create_video_with_waterMark
from pdf2image import convert_from_path
from PIL import Image
#影片用
#
######## 1.生成水印pdf的函式 ########
def create_watermark_Horizontal(content, markPDFPath='mark-h.pdf', imagePath='qrcode.png'):
    # 預設大小為21cm*29.7cm
    c = canvas.Canvas(markPDFPath, pagesize=(30 * cm, 30 * cm))
    c.translate(10 * cm,
                10 * cm)  # 移動座標原點(座標系左下為(0,0)))
    c.setFont('NotoSansCJKtc-Medium', 18)  # 設定字型為宋體，大小22號
    c.drawImage(imagePath, 608, -270, width=60, height=60)
    c.setFillColorRGB(20, 0.5, 0.5)  # 灰色
    c.drawString(-9 * cm, 8 * cm, "CY")
    c.setFillColorRGB(0.8, 0.8, 0.8)  # 灰色

    c.rotate(45)  # 旋轉45度，座標系被旋轉

    #0
    c.drawString(-4 * cm, 9 * cm, content)
    c.drawString(0 * cm, 4 * cm, content)
    c.drawString(6 * cm, -1 * cm, content)
    c.drawString(10 * cm, -5 * cm, content)
    c.drawString(15 * cm, -10 * cm, content)
    #1
    c.drawString(-6 * cm, 2 * cm, content)
    c.drawString(-1 * cm, -3 * cm, content)
    c.drawString(4 * cm, -7 * cm, content)
    c.drawString(9 * cm, -13 * cm, content)
    #2
    c.drawString(-14 * cm, 0 * cm, content)

    c.drawString(-8 * cm, -4 * cm, content)
    c.drawString(-4 * cm, -10 * cm, content)

    c.drawString(2 * cm, -15 * cm, content)
    c.drawString(7 * cm, -20 * cm, content)

    # c.drawString(-2 * cm, 9 * cm, content)
    # c.drawString(-2 * cm, -9 * cm, content)
    # 旋轉45度，座標系被旋轉
    c.save()  # 關閉並儲存pdf檔案

def create_watermark_Straight(content, markPDFPath='mark-s.pdf', imagePath='qrcode.png'):
    # 預設大小為21cm*29.7cm
    c = canvas.Canvas(markPDFPath, pagesize=(30 * cm, 30 * cm))
    c.translate(10 * cm,
                10 * cm)  # 移動座標原點(座標系左下為(0,0)))
    c.setFont('NotoSansCJKtc-Medium', 18)  # 設定字型為宋體，大小22號
    c.drawImage(imagePath, 250, -280, width=60, height=60)
    c.setFillColorRGB(20, 0.5, 0.5)  # 灰色
    c.drawString(-10 * cm, 19 * cm, "CY")
    c.setFillColorRGB(0.8, 0.8, 0.8)  # 灰色
    c.rotate(45)  # 旋轉45度，座標系被旋轉

    #0
    c.drawString(4 * cm, 17 * cm, content)
    c.drawString(8 * cm, 13 * cm, content)
    c.drawString(12 * cm, 9 * cm, content)
    c.drawString(16 * cm, 5 * cm, content)
    #1
    c.drawString(0 * cm, 13 * cm, content)
    c.drawString(4 * cm, 9 * cm, content)
    c.drawString(8 * cm, 5 * cm, content)
    c.drawString(12 * cm, 1 * cm, content)

    #2
    c.drawString(-4 * cm, 9 * cm, content)
    c.drawString(0 * cm, 4 * cm, content)
    c.drawString(6 * cm, -1 * cm, content)
    c.drawString(10 * cm, -5 * cm, content)
    c.drawString(15 * cm, -10 * cm, content)
    #3
    c.drawString(-6 * cm, 2 * cm, content)
    c.drawString(-1 * cm, -3 * cm, content)
    c.drawString(4 * cm, -7 * cm, content)
    c.drawString(9 * cm, -13 * cm, content)
    #4
    c.drawString(-14 * cm, 0 * cm, content)
    c.drawString(-8 * cm, -4 * cm, content)
    c.drawString(-4 * cm, -10 * cm, content)
    c.drawString(2 * cm, -15 * cm, content)
    c.drawString(7 * cm, -20 * cm, content)

    # c.drawString(-2 * cm, 9 * cm, content)
    # c.drawString(-2 * cm, -9 * cm, content)
    # 旋轉45度，座標系被旋轉
    c.save()  # 關閉並儲存pdf檔案

def create_watermark_video(content, markPDFPath='mark.pdf', imagePath='qrcode.png'):
    # 預設大小為21cm*29.7cm
    c = canvas.Canvas(markPDFPath, pagesize=(30 * cm, 30 * cm))
    c.translate(10 * cm,
                10 * cm)  # 移動座標原點(座標系左下為(0,0)))
    c.setFont('NotoSansCJKtc-Medium', 18)  # 設定字型為宋體，大小22號
    c.drawImage(imagePath, 250, -280, width=60, height=60)
    c.setFillColorRGB(20, 0.5, 0.5)  # 灰色
    c.drawString(-10 * cm, 19 * cm, "CY")
    c.setFillColorRGB(0.8, 0.8, 0.8)  # 灰色
    c.setFillAlpha(0.3)
    c.rotate(45)  # 旋轉45度，座標系被旋轉

    #0
    c.drawString(4 * cm, 17 * cm, content)
    c.drawString(8 * cm, 13 * cm, content)
    c.drawString(12 * cm, 9 * cm, content)
    c.drawString(16 * cm, 5 * cm, content)
    #1
    c.drawString(0 * cm, 13 * cm, content)
    c.drawString(4 * cm, 9 * cm, content)
    c.drawString(8 * cm, 5 * cm, content)
    c.drawString(12 * cm, 1 * cm, content)

    #2
    c.drawString(-4 * cm, 9 * cm, content)
    c.drawString(0 * cm, 4 * cm, content)
    c.drawString(6 * cm, -1 * cm, content)
    c.drawString(10 * cm, -5 * cm, content)
    c.drawString(15 * cm, -10 * cm, content)
    #3
    c.drawString(-6 * cm, 2 * cm, content)
    c.drawString(-1 * cm, -3 * cm, content)
    c.drawString(4 * cm, -7 * cm, content)
    c.drawString(9 * cm, -13 * cm, content)
    #4
    c.drawString(-14 * cm, 0 * cm, content)
    c.drawString(-8 * cm, -4 * cm, content)
    c.drawString(-4 * cm, -10 * cm, content)
    c.drawString(2 * cm, -15 * cm, content)
    c.drawString(7 * cm, -20 * cm, content)

    # c.drawString(-2 * cm, 9 * cm, content)
    # c.drawString(-2 * cm, -9 * cm, content)
    # 旋轉45度，座標系被旋轉
    c.save()  # 關閉並儲存pdf檔案
    images = convert_from_path(markPDFPath)
    images[0].save('./personalData/' + content + '/watermark.png', 'JPEG')
    image = Image.open('./personalData/' + content + '/watermark.png')
    image = image.convert('RGBA')
    # Transparency
    newImage = []
    for item in image.getdata():
        if item[0] >= 240:
            newImage.append((255, 255, 255, 0))
        else:
            newImage.append(item)
    image.putdata(newImage)
    image.save('./personalData/' + content + '/watermark.png')

######## 2.為pdf檔案加水印的函式 ########
def add_watermark2pdf(input_pdf, output_pdf, watermark_pdf,scale):
    watermark = PdfFileReader(watermark_pdf)
    # qrcode = PdfFileReader(qrcode_pdf)

    watermark_page = watermark.getPage(0)
    pdf = PdfFileReader(input_pdf, strict=False)
    pdf_writer = PdfFileWriter()
    # print(pdf.getPage(0).mediaBox.getHeight())

    for page in range(pdf.getNumPages()):
        pdf_page = pdf.getPage(page)
        pdf_page.scaleBy(scale)
        pdf_page.mergePage(watermark_page)
        # pdf_page.mergePage(qrcode)

        pdf_writer.addPage(pdf_page)
    pdfOutputFile = open(output_pdf, 'wb')
    # pdf_writer.encrypt('scb2018')  # 設定pdf密碼
    pdf_writer.write(pdfOutputFile)
    pdfOutputFile.close()

######## 2.為pdf檔案加水印的函式 ########
def scale_pdf(input_pdf, output_pdf,scale):
    # qrcode = PdfFileReader(qrcode_pdf)

    pdf = PdfFileReader(input_pdf, strict=False)
    pdf_writer = PdfFileWriter()
    # print(pdf.getPage(0).mediaBox.getHeight())

    for page in range(pdf.getNumPages()):
        pdf_page = pdf.getPage(page)
        pdf_page.scaleBy(scale)
        # pdf_page.mergePage(qrcode)
        pdf_writer.addPage(pdf_page)

    pdfOutputFile = open(output_pdf, 'wb')
    # pdf_writer.encrypt('scb2018')  # 設定pdf密碼
    pdf_writer.write(pdfOutputFile)
    pdfOutputFile.close()

def create_PDF_without_water(username, rawPDFPath, outputPDFPath):

    pageBroadwise = (PdfFileReader(rawPDFPath).getPage(0).mediaBox.getHeight()) < PdfFileReader(rawPDFPath).getPage(0).mediaBox.getWidth()

    if pageBroadwise:

        scale = float(1000/PdfFileReader(rawPDFPath).getPage(0).mediaBox.getWidth())

    else:
        scale = float(1000/PdfFileReader(rawPDFPath).getPage(0).mediaBox.getHeight())


    scale_pdf(rawPDFPath, rawPDFPath + 'tmp',scale=scale)
    sources = []
    images = convert_from_path(rawPDFPath + 'tmp')
    output = images[0]
    images.pop(0)
    for image in images:
        pngFile = image
        if pngFile.mode == "RGB":
            pngFile = pngFile.convert("RGB")
        sources.append(pngFile)
    output.save(outputPDFPath, "pdf", save_all=True, append_images=sources)
    os.remove(rawPDFPath + 'tmp')
    os.remove(rawPDFPath)
def create_PDF_water(username, rawPDFPath, outputPDFPath):
    if not os.path.exists('./personalData/' + username + '/qrcode.png'):
        createQR(username + "\n" + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"),savePath='./personalData/' + username + '/qrcode.png')
    # .scaleBy(0.5)
    pageBroadwise = (PdfFileReader(rawPDFPath).getPage(0).mediaBox.getHeight()) < PdfFileReader(rawPDFPath).getPage(0).mediaBox.getWidth()

    if pageBroadwise:

        scale = float(1000/PdfFileReader(rawPDFPath).getPage(0).mediaBox.getWidth())
        markPath = "./personalData/"+username+"/mark-h.pdf"
        if not os.path.exists("./personalData/"+username+"/mark-h.pdf"):
                create_watermark_Horizontal(username,markPDFPath="./personalData/"+username+"/mark-h.pdf")  # 創造了一個水印pdf：mark.pdf
    else:
        scale = float(1000/PdfFileReader(rawPDFPath).getPage(0).mediaBox.getHeight())
        markPath = "./personalData/" + username + "/mark-s.pdf"
        if not os.path.exists("./personalData/"+username+"/mark-s.pdf"):
                create_watermark_Straight(username,markPDFPath="./personalData/"+username+"/mark-s.pdf")

    add_watermark2pdf(rawPDFPath, rawPDFPath + 'tmp', markPath,scale=scale)
    sources = []
    images = convert_from_path(rawPDFPath + 'tmp')
    output = images[0]
    images.pop(0)
    for image in images:
        pngFile = image
        if pngFile.mode == "RGB":
            pngFile = pngFile.convert("RGB")
        sources.append(pngFile)
    output.save(outputPDFPath, "pdf", save_all=True, append_images=sources)
    os.remove(rawPDFPath + 'tmp')
def create_mp4_water(username, rawVideoPath, outputVideoPath):
    if not os.path.exists('./personalData/' + username + '/qrcode.png'):
        createQR(username + "\n" + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S"),savePath='./personalData/' + username + '/qrcode.png')
    if not os.path.exists('./personalData/"+username+"/mark-v.pdf'):
        create_watermark_video(username,markPDFPath="./personalData/"+username+"/mark-v.pdf")
    create_video_with_waterMark(rawVideoPath=rawVideoPath,outputVideoPath=outputVideoPath,qrcodePath='./personalData/' + username + '/qrcode.png',waterMarkPath='./personalData/' + username + '/watermark.png')


if __name__ == '__main__':

    # create_PDF_water("CYP_AA測試人員", "空白.pdf", "空白有浮水印.pdf")
    create_mp4_water("CYP_AA測試人員","清潔少了這個觀念，小心洗臉越洗越糟！-凱穎","測試影片.mp4")


