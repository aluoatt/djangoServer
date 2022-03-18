

import qrcode # 匯入模組
from PIL import Image
def createQR(message,savePath):
    # img = qrcode.make(message)  # QRCode資訊
    # img.save("qrcode.png")  # 儲存圖片
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(message)
    qr.make(fit=True)

    img = qr.make_image()
    img.save(savePath)