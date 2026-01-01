from db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SHOW TABLES")

print("Tables in your_database_name:")
for table in cursor:
    print(table)

conn.close()
