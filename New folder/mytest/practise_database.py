from database import get_connection

conn=get_connection()
cursor=conn.cursor()


#Select all records from the "admin" table, and display the result:
"""cursor.execute("select * from admin")
results=cursor.fetchall()
print(results)"""

# see individual colums
""" cursor.execute("select name, password from admin")
results=cursor.fetchall()
print(results) """

cursor.execute("SELECT * FROM admin  ORDER BY name DESC")
results=cursor.fetchall()
print(results)





















cursor.close()
conn.close()

