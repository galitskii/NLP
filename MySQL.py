'''
Установка с базой данных MySQL и вывод данных оттуда
'''
import mysql.connector
from mysql.connector import Error

conn = mysql.connector.connect(host='localhost', user='lexis', password='lexis', database = 'lexis')

with conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM CASE_OF_WORD")
    rows = cur.fetchall()
    for row in rows:
        print(row)
        
cur.close()
conn.close()