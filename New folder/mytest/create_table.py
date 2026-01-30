from database import get_connection
conn =get_connection()
cursor=conn.cursor()

# cursor.execute("""
#     CREATE TABLE admin ( 
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(50) unique, 
#     password VARCHAR(20), 
#     role VARCHAR(20),
#     is_active BOOLEAN DEFAULT TRUE)""")

# print("table created successfully")




# cursor.execute("""
#     # CREATE TABLE users( 
#     # id INT AUTO_INCREMENT PRIMARY KEY,
#     # fullname VARCHAR(50),
#     # username VARCHAR(50) unique, 
#     # password VARCHAR(20),
#     # email varchar(50),
#     # phone int (15),
#     # gender varchar(10),          
#     # role VARCHAR(20),
#     # is_active BOOLEAN DEFAULT TRUE)""")
    

# print("table created successfully")

cursor.execute("ALTER TABLE users MODIFY phone VARCHAR(15);")
