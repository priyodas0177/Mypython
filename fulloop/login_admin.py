from database import get_connection
from admin_panel import AdminPanel   # <-- import the class (OOP), not admin_func
from user_panel import User_panel


class AdminAuth:
    def __init__(self):
        pass

    def login(self):
        username = input("Enter User name: ")
        password = input("Enter Your Password: ")

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT id, name, role 
        FROM admin 
        WHERE name=%s AND password=%s AND is_active=1
        """
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if not result:
            print("Invalid Username / password or inactive account ")
            return False
        
        user_id, uname, role=result
        print(f"\nWelcome {uname} ({role})")

        if role=="admin":
            AdminPanel(user_id,uname).show_menu()
        else:
            User_panel(user_id,uname,role).show_menu()

        # if result:
        #     admin_id, admin_name,role = result
        #     print(f"\nWelcome Admin: {admin_name}")

        #     # Start admin panel (OOP)
        #     panel = AdminPanel(admin_id, admin_name)
        #     panel.show_menu()
        #     return True
        # else:
        #     print("Invalid User")
        #     return False


if __name__ == "__main__":
    auth = AdminAuth()
    auth.login()
