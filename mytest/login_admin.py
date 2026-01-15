from database import get_connection
from admin_panel import admin_func

def admin_Login():
    username=input("Enter User name: ")
    password=input("Enter Your Password: ")

    conn=get_connection()
    curser=conn.cursor()
  

    sql="""select id, name from admin where name=%s and
    password=%s and is_active=1"""

    curser.execute(sql, (username, password))
    result=curser.fetchone()

    curser.close()
    conn.close()

    if result:
        admin_id=result[0]
        admin_name=result[1]
        print(f"\n Welcome Admin:")
        print(f"\n Welcome Admin: {admin_name}")
        admin_func(admin_id,admin_name)
        
    else:
        print(f"\n Welcome Admin: ")
        print("Invalid User")
        return None
admin_Login()
