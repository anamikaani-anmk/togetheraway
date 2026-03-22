import mysql.connector
from mysql.connector import Error

def get_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="together_user",       
            password="mypassword123",   
            database="togetheraway"     
        )
        return conn
    except Error as e:
        print("Database connection failed:", e)
