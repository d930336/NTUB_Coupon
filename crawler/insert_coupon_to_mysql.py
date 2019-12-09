import requests
from bs4 import BeautifulSoup
import os
from urllib.request import urlretrieve
import pandas as pd

#資料庫存檔
import mysql.connector
from insert_mysql import prevent_duplicate
from password import My_password

#建立資料庫連線
mydb = mysql.connector.connect(
    user='root',
    passwd=My_password,
    host='localhost',
    database='mangerdb',
)

mycursor = mydb.cursor()
mycursor.execute('use mangerdb')

url = "https://www.4freeapp.com/"
respond = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
html = BeautifulSoup(respond.text)
main = html.find_all("div", class_="caption")

# 準備空的 dataFrame
df = pd.DataFrame(columns=['id', 'title', 'class', 'content'])
df1 = pd.DataFrame(columns=['title', 'adress'])

# 儲存網頁內所有內容
add_String = ''
add_Tag = ''

today_judge = ''


# 判斷檔名
def judge(x):
    if "jpg" in x or "png" in x:
        return True
    else:
        return False


for _ in main:
    index_title = _.find("a").string  # 這個會有\n
    index_url = _.find("a").get("href")

    # 直接使用網站的title會有\n的問題，所以要先排除\n或\造成的錯誤("\"會造成註解)
    Index_Title = index_title.split('\n')[1]
    # judge the url
    today_judge = index_url

    index_respond = requests.get(index_url, headers={'User-agent': 'Mozilla/5.0'})
    index_html = BeautifulSoup(index_respond.text)
    index_main = index_html.find_all("a", attrs={'style': 'margin-left: 1em; margin-right: 1em;'})

    # 網頁內容
    index_content = index_html.find_all("span", attrs={'style': 'font-size: large;'})

    # 網頁 tag
    index_tag = index_html.find_all("div", class_="widget-tags")

    # MySQL Myclass
    for text in index_tag:
        print(Index_Title)
        text_a = text.find_all("a")

        for str in text_a:
            # 物件類別
            class_tab = str.string
            web_tag = class_tab.split("\n")[1]
            add_Tag = add_Tag + web_tag + "/"

    # MySQL content
    for text in index_content:
        if text.string is not None:
            # add_text.append(text.string.splitlines())
            # splitlines將\n分開
            add_String = add_String + text.string.splitlines()[0] + "\ "

    # MySQL ID
    for i in index_main:
        downloadURL = i.get("href")
        ds = downloadURL.split("/")
        ##設定ID
        coupon_id = ds[5]

        #將資料輸入進資料庫
        prevent_duplicate(coupon_id, Index_Title.splitlines()[-1], add_Tag, add_String)

        #將資料存入DataFrame
        s = pd.Series([coupon_id, Index_Title.splitlines()[-1], add_Tag, add_String],
                      index=['id', 'title', 'class', 'content'])
        df = df.append(s, ignore_index=True)

    # 重製儲存字串
    add_String = ''
    add_Tag = ''

    # 儲存圖片
    for i in index_main:
        # 設定資料夾路徑，怕標題有/
        dname = "C:/Users/Jun/Desktop/coupon/" + Index_Title.split("/")[0] + "/"

        if not os.path.exists(dname):
            os.mkdir(dname)

        downloadURL = i.get("href")
        print(downloadURL)
        ds = downloadURL.split("/")
        filetype = ds[-1].split(".")[-1]
        judgeURL = filetype

        if judgeURL:
            fpath = dname + ds[5] + "." + filetype
            urlretrieve(downloadURL, fpath)

        s1 = pd.Series([Index_Title.splitlines()[-1], fpath], index=['title', 'adress'])
        df1 = df1.append(s1, ignore_index=True)

print("判斷標準", today_judge)

import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d")
now = now.split("-")
begin = datetime.date(int(now[0]), int(now[1]), int(now[2]))
end = datetime.date(2019, 5, 11)
d = begin
delta = datetime.timedelta(days=1)

while d >= end:
    print(d.strftime("%Y-%m-%d"))
    url = "https://www.4freeapp.com/search?updated-max=" + d.strftime(
        "%Y-%m-%d") + "T10%3A53%3A00%2B08%3A00&max-results=7#PageNo=2"
    respond = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})

    html = BeautifulSoup(respond.text)
    main = html.find_all("div", class_="caption")

    # 網頁內容
    index_content = index_html.find_all("span", attrs={'style': 'font-size: large;'})
    # 網頁 tag
    index_tag = index_html.find_all("div", class_="widget-tags")

    for times in reversed(main):
        index_title = times.find("a").string  # 這個會有\n
        index_url = times.find("a").get("href")
        Index_Title = index_title.split('\n')[1]  ##把indextitle的\n排除

        if today_judge == index_url:
            today_judge = main[-1].find("a").get("href")
            break

        print("頁尾", main[-1].find("a").get("href"))
        print("判斷標準", today_judge)
        print(Index_Title)

        index_respond = requests.get(index_url, headers={'User-agent': 'Mozilla/5.0'})
        index_html = BeautifulSoup(index_respond.text)
        index_main = index_html.find_all("a", attrs={'style': 'margin-left: 1em; margin-right: 1em;'})

        # 網頁內容
        index_content = index_html.find_all("span", attrs={'style': 'font-size: large;'})

        # 將標題和內容存成CSV
        for text in index_content:
            if text.string is not None:
                # add_text.append(text.string.splitlines())
                # splitlines將\n分開
                add_String = add_String + text.string.splitlines()[0] + "\ "

        # MySQL Myclass
        for text in index_tag:
            print(Index_Title)
            text_a = text.find_all("a")

            for str in text_a:
                # 物件類別
                class_tab = str.string
                web_tag = class_tab.split("\n")[1]
                add_Tag = add_Tag + web_tag + "/"
        # MySQL ID
        for i in index_main:
            downloadURL = i.get("href")
            ds = downloadURL.split("/")
            ##設定ID
            coupon_id = ds[5]
            print(coupon_id)

            # 將資料輸入進資料庫
            prevent_duplicate(coupon_id, Index_Title.splitlines()[-1], add_Tag, add_String)

            #將資料存進DataFrame
            s = pd.Series([coupon_id, Index_Title.splitlines()[-1], add_Tag, add_String],
                          index=['id', 'title', 'class', 'content'])
            df = df.append(s, ignore_index=True)

        # 重製儲存字串
        add_String = ''
        add_Tag = ''

        ##儲存
        for i in index_main:
            print(Index_Title)
            # 設定資料夾路徑，怕標題有/
            dname = "C:/Users/Jun/Desktop/coupon/" + Index_Title.split("/")[0] + "/"
            if not os.path.exists(dname):
                os.mkdir(dname)

            downloadURL = i.get("href")
            print(downloadURL)

            ds = downloadURL.split("/")
            filetype = ds[-1].split(".")[-1]
            if judge(filetype):
                fpath = dname + ds[5] + "." + filetype
                urlretrieve(downloadURL, fpath)

            s1 = pd.Series([Index_Title.splitlines()[-1], fpath], index=['title', 'adress'])
            df1 = df1.append(s1, ignore_index=True)

    d -= delta
print(df)
print(df1)
df.to_csv("title_content.csv", encoding='utf-8', index=False)
df1.to_csv("title_address.csv", encoding='utf-8', index=False)