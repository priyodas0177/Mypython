import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@H.dpriyo0177@.",
        database="company_db"
    )
print("Databse Connected. ")