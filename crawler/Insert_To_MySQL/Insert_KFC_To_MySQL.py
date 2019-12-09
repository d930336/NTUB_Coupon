import mysql.connector
from Coupon_Backend_Final.crawler.password import My_password
from Excel_To_SQL import limit_unicode , Convert_Excel_To_MySQL

#建立資料庫連線
mydb = mysql.connector.connect(
    user='root',
    passwd=My_password,
    host='127.0.0.1',
    database='ntub_project',
    auth_plugin='mysql_native_password'
)


My_Excel = Convert_Excel_To_MySQL("KFC1104.xlsx")

#取得Excel資料
My_Excel.Set_DataSet()

#連線進資料庫
My_Excel.Connect_To_Sql(mydb,"ntub_project")

# 取得SQl字串
My_Excel.Get_InsertSQL("api_coupon" , ["coupon_id","coupon_title","coupon_note",
                                                "coupon_notice","coupon_price","coupon_original_price",
                                              "coupon_img" , "coupon_class" ,"coupon_create_at","coupon_saving"])

# print(My_Excel.df["original price"])
print(My_Excel.dataset)
print(My_Excel.insert_sql)

My_Excel.Bulk_Insert()