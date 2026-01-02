from database import get_connection
conn =get_connection()
cursor=conn.cursor()

cursor.execute("""
    CREATE TABLE admin ( 
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) unique, 
    password VARCHAR(20), 
    role VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE)""")

print("table created successfully")
