import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="todouser",
        password="user@%1289$",
        database="Todo"
    )
