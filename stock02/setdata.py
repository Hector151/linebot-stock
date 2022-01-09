import os
import psycopg2

DB_url = os.popen('heroku config:get DATE_url -a stock-bot:v2').read()[:-1]
conn = psycopg2.connect(DB_url, sslmode = 'require')
cursor = conn.cursor()
SQL_order = '''CREATE TABLE account(
    user_id serial PRIMARY KEY,
    
);'''
cursor.execute(SQL_order)

conn.commit()

cursor.close()
conn.close()

print("success")
