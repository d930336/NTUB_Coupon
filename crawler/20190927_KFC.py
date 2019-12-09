import requests
from bs4 import BeautifulSoup
import shutil
import pandas as pd
from Log import ErrorWrite
import datetime
from PIL import Image
from Convert_Img import convert_Image , change_Image_to_text

# connect to web
url = "https://www.kfcclub.com.tw/tw/Coupon/"
respond = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
html = BeautifulSoup(respond.text)
main = html.find_all('div',attrs={'style': 'cursor:pointer;text-align:center'})

#   df -> 'coupon_id' , '標題' , '內文' , '注意事項'
df = pd.DataFrame(columns=['id', 'title', 'note', 'notice' , 'price'])

# log 檔案名稱
log_file_name = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S') + '.txt'

#計算現在為第幾筆
cnt = 1

# 從屬性尋找要爬蟲的資料
for item in main:
    img_src = item.find("img")['src']
    img_name = item.find("img")['code']

    # 網頁內容
    title = item.find("img")['t']
    note = item.find_all("p")
    expire_date = ""
    for expire in note:
        expire_date = expire_date + expire.text
    notice = item.find("img")['onclick'].split(',')[3]

    #------------寫入pd和檢查是否有空值--------------
    if not img_name or not title or not expire_date or not notice:
        ErrorWrite(log_file_name,"第{0}筆資料，欄位出現空值\n".format(cnt))

    #------------儲存圖片--------------
    r = requests.get(img_src, stream=True, headers={'User-agent': 'Mozilla/5.0'})  # stream=True 则会推迟响应内容的下载
    img_path = "C:/Users/case-pc/Desktop/KFC/" + img_name + ".jpg"
    if r.status_code == 200:
        with open(img_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    #-------------辨識價格-----------------
    img = Image.open(img_path)

    # 剪裁圖片
    img = img.crop((35, 70, 100, 105))
    img = convert_Image(img) #二值化
    price = change_Image_to_text(img) #數字辨識

    #---------------------------儲存資料-----------------------
    s = pd.Series([img_name, title, expire_date, notice,price],
                  index=['id', 'title', 'note', 'notice' , 'price'])
    df = df.append(s, ignore_index=True)
    cnt = cnt + 1

df.to_excel("KFC.xlsx", encoding='utf-8', index=False)

