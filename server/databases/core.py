import mysql.connector
import sys
sys.path.append('../')
import config


class DB:
    def __init__(self):
        self.host = config.MYSQL_HOST
        self.user = config.MYSQL_USER
        self.password = config.MYSQL_PASSWORD
        self.database = config.MYSQL_DATABASE_NAME
    def conn(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=config.MYSQL_PORT,
                # ssl_ca = './ca.pem'
            )
            return conn
        except mysql.connector.Error as err:
            print("Lỗi: {}".format(err))
            return None

    def select_data(self, query,params):
        conn = self.conn()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                results = cursor.fetchall()
                cursor.close()
                conn.close()
                return results
            except mysql.connector.Error as err:
                print("Lỗi truy vấn: {}".format(err))
                return None

    def insert_data(self, query, params):
        conn = self.conn()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
                cursor.close()
                conn.close()
                print("Dữ liệu đã được chèn thành công.")
            except mysql.connector.Error as err:
                print("Lỗi truy vấn: {}".format(err))
                conn.rollback()  # Hoàn tác thay đổi nếu có lỗi
                cursor.close()
                conn.close()
    def update(self, query, params):
        conn = self.conn()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()  
                cursor.close()
                conn.close()
            except mysql.connector.Error as err:
                print("Lỗi truy vấn: {}".format(err))
                conn.rollback()  
                cursor.close()
                conn.close()
    def delete(self, query, params):
        conn = self.conn()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()  
                cursor.close()
                conn.close()
                print("Dữ liệu đã được xóa thành công.")
            except mysql.connector.Error as err:
                print("Lỗi truy vấn: {}".format(err))
                conn.rollback()  # Hoàn tác thay đổi nếu có lỗi
                cursor.close()
                conn.close()
    def drop(self, tablename):
        conn = self.conn()
        query = f"drop table if exists {tablename}"
        if conn:
            try: 
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                cursor.close()
                conn.close()
                
            except mysql.connector.Error as err:
                print("Lỗi truy vấn: {} -> {}".format(query, err))
                conn.rollback()  # Hoàn tác thay đổi nếu có lỗi
                cursor.close()
                conn.close()
    def create_table(self, query):
        conn = self.conn()
        if conn:
            try: 
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                cursor.close()
                conn.close()
                
            except mysql.connector.Error as err:
                print("Lỗi truy vấn: {} -> {}".format(query, err))
                conn.rollback()  # Hoàn tác thay đổi nếu có lỗi
                cursor.close()
                conn.close()

