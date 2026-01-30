from database import get_connection
from admin_panel import AdminPanel
from user_panel import User_Panel

class AuthService:
    def admin_Login(self):
        username=input("Enter User name: ")
        password=input("Enter Your Password: ")

        conn=get_connection()
        curser=conn.cursor()

        #(1) Admin Login
        admin_sql="""select id, name from admin where name=%s and
            password=%s and is_active=1"""

        curser.execute(admin_sql, (username, password))
        result=curser.fetchone()
         
        if result:
            admin_id, admin_name=result
            curser.close()
            conn.close()

            print(f"\nWelcome Admin: {admin_name}")
            AdminPanel(admin_id, admin_name).show_menu()
            return True
        
        #(2) User Login
        user_sql="""SELECT id, username, role
                FROM users WHERE username=%s and password=%s AND is_active=1
                """
        
        curser.execute(user_sql,(username,password))
        result_user=curser.fetchone()
        curser.close()
        conn.close()

        if result_user:
            user_id,username,role=result_user
            #print(f"\nWelcome {username}")
            User_Panel(user_id,username,role).show_menu()
            return True
        print("Invalid User")
        

if __name__ == "__main__":
    AuthService().admin_Login()