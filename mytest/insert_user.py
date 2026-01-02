from database import get_connection

conn = get_connection()
curser =conn.cursor()

sql="""insert into admin (name, password, role, is_active) 
values (%s, %s, %s, %s)
"""
curser.execute(sql, ("pallab", "pal123", "admin", 1))
conn.commit()

print("admin created successfully")
curser.close()
conn.close()

