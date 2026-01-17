from database import get_connection

conn = get_connection()
cursor = conn.cursor()

"""cursor.execute("SELECT * FROM admin")

rows = cursor.fetchall()

print("\nUsers Table Data:\n")
for row in rows:
    print(row)"""

cursor.execute("show tables from testdb")

cursor.close()
conn.close()
 