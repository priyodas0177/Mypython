#from database import get_connection
from Status import user_status_menu
from user import create_user
from view import view_admin_users,view_users
from update import update_user
from delete import delete_user

class AdminPanel:
    def __init__(self,admin_id,admin_name):
        self.admin_id=admin_id
        self.admin_name=admin_name
    
    def show_menu(self):    
        print(f"\n=====ADMIN PANEL=====")
        print(f"Welcome, {self.admin_id,self.admin_name}")
        print("1. Create User")
        print("2. View Admin Users")
        print("3. view Users")
        print("4. Update User")
        print("5. User Status ")
        print("6. Delete User")
        print("7. Logout")

        choice= input("Enter your choice (1-5):")
        if choice== "1":
            create_user()
        elif choice=="2":
            view_admin_users()
        elif choice=="3":
            view_users()
        elif choice=="4":
            update_user()
        elif choice=="5":
            user_status_menu()
        elif choice=="6":
            delete_user(self.admin_id)
        elif choice=="7":
            print("Logging out...")
        else:
            print("Invalid choice. Please try again.")





   
        







    

 
    

        



        
