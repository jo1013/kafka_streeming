import mysql.connector
from mysql.connector import Error
import random
import time
from datetime import datetime
import os

# MySQL 데이터베이스 연결 설정
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            port=os.getenv('MYSQL_PORT'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"Error: '{e}'")
    return connection

# 주문 데이터 삽입 함수
def insert_order(connection, order_date, status):
    cursor = connection.cursor()
    query = "INSERT INTO orders (order_date, status) VALUES (%s, %s)"
    values = (order_date, status)
    cursor.execute(query, values)
    connection.commit()
    print(f"Inserted order: {order_date}, {status}")

# 임의의 주문 상태 생성
def generate_status():
    statuses = ['pending', 'completed', 'canceled']
    return random.choice(statuses)

# 실시간 데이터 생성 및 삽입
def generate_orders(connection):
    while True:
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = generate_status()
        insert_order(connection, order_date, status)
        time.sleep(1)  # 1초마다 새로운 주문 생성

# 메인 함수
def main():
    connection = create_connection()
    if connection:
        generate_orders(connection)

if __name__ == "__main__":
    main()