# dbconnection.py
import pymysql

def get_connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='mydb'
    )
    return conn