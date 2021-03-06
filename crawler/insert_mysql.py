import mysql.connector
import datetime


class Set_Mysql():
    def __init__(self,_id,_title,_class,_content , _conn , _db):
        self._id = _id
        self._title = _title
        self._class = _class
        self._content = _content
        self._conn = _conn
        self._db = _db
    def Connect_To_Sql(self):
        """
                連線到資料庫
                """
        self._my_cursor = self._conn.cursor()
        self._my_cursor.execute('use ' + str(self._db))
    def prevent_duplicate(self):
        """
                輸入進資料庫
                """
        title_data = (self._title,)
        sql = "select * from mangerdb_item where title = %s"
        self._my_cursor.execute(sql, title_data)
        my_result = self._my_cursor.fetchall()
        if my_result:
            print('重複的資料', 'id', id, '標題', title_data[0])
        else:
            try:
                insert_sql = "insert ignore into mangerdb_item (id , title ,Myclass , content) values (%s,%s,%s,%s)"
                insert_data = (self._id, self._title, self._class, self._content)
                self._my_cursor.execute(insert_sql, insert_data)
                self._conn.commit()
            except mysql.connector.Error as error:
                self._conn.rollback()
            finally:
                if self._my_cursor.rowcount:
                    print("資料成功輸入")
                else:
                    time_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    insert_data = (self._id, self._title, self._class, self._content)
                    self._my_cursor.execute(insert_sql, insert_data)
                    self._conn.commit()
                    print(self._my_cursor.rowcount, "record inserted.", "id改為時間參數")