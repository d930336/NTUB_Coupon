import pytesseract
import re
from PIL import Image


#去雜訊
def convert_Image(img,standard=127.5):
    """
            轉換成灰階
        """
    image = img.convert('L')

    """
      二值化
      -> 根據閥值standard , 將所有像素都置為 0(黑色) 或 255(白色), 便於接下來的分割
    """
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y] > standard:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return image


#使用 pytesseract 庫來識別圖片中的字符
def change_Image_to_text(img):
    """"
            如果出現 使用pytesseract出现错误：“[WinError 2] 系统找不到指定的文件
            則需要手動設定路徑，將 testdata_dir_config 和  tesseract_cmd 設定成自己下載的tesseract.exe所在路徑
            tesseract.exe download  -> https://github.com/UB-Mannheim/tesseract/wiki
            ref - > https://blog.csdn.net/jacke121/article/details/75443785
        """
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    testdata_dir_config = "C:\Program Files\Tesseract-OCR\tesseract.exe"
    textCode = pytesseract.image_to_string(img, lang='eng', config=testdata_dir_config)
    # 去掉非法字符，只保留字母數字
    textCode = re.sub("\W", "", textCode)
    return textCode