import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@H.dpriyo0177@.",
        database="test_db"
    )
print("Databse Connected. ")

"""import mysql.connector
from mysql.connector import Error  # import Error properly

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@H.dpriyo0177@.",
        database="testdb"
    )

    if conn.is_connected():
        print("Connection to my database successful.")

        mycursor = conn.cursor()

        mycursor.execute(""""""""""""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE,
                password VARCHAR(20),
                role VARCHAR(20),
                is_active BOOLEAN DEFAULT TRUE
            )
        """""""""""")
        print("Table is created successfully.")

except Error as e:
    print("Error:", e)

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("Connection closed.")"""
