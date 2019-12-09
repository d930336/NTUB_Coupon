import pandas as pd
import mysql.connector
from Coupon_Backend_Final.crawler.password import My_password
import re

# 切割特殊符號，使內容只剩下中文，英文，數字
# ref ----> https://www.jianshu.com/p/a5aa570d8173
def limit_unicode(text):
    # 抓出不是中文 ， 英文 ，數字的符號
    cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^)^(^\uff0c^;^\^/^.^:^\u0020^-]")

    # 将抓到的符號替换成空白
    result = cop.sub('', text)
    return result

class Convert_Excel_To_MySQL():
    def __init__(self,file_path):
        self.file_path = file_path
        self.df = pd.read_excel(file_path).dropna(thresh=3)
        self.col = list(self.df.columns)
    def Set_DataSet(self):
        """
                將 Excel的資料轉成Tuple
                """
        arr = []
        for i in self.df.index:
            row_val = []
            for col in self.col:
                row_val.append(limit_unicode(str(self.df[col][i])))
            arr.append(tuple(row_val))
        self.dataset = arr
    def Connect_To_Sql(self, conn , db):
        """
                連線到SQL
                :param conn: 連線進資料庫
                :param db: 資料庫名稱
                """
        self._conn = conn
        self._db = db
        self._mycursor = self._conn.cursor()
        self._mycursor.execute('use ' + str(self._db))
    def Get_InsertSQL(self , tb ,colSet):
        """
                取得SQL字串
                :param tb: 資料表名稱
                :param colSet:  欄位
                """
        sql = "insert into "+str(tb) + "("
        sql_value = ""
        for db_col in colSet:
            sql = sql + " " + str(db_col)
            sql_value += "%s "
            if(db_col != colSet[-1]):
                sql += ","
                sql_value += ","
        sql += ") value "
        sql = sql + "( " + sql_value + ")"
        self.insert_sql = sql
    def Bulk_Insert(self):
        try:
            self._mycursor.executemany(self.insert_sql, self.dataset)
            self._conn.commit()
        except mysql.connector.Error as error:
            print(error)
            self._conn.rollback()
    def Close_Conn(self):
        self._mycursor.close()
        self._conn.close()








