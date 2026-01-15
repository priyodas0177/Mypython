from database import get_connection

def admin_func(admin_id, admin_name):
    while True:
        print("=====ADMIN PANEL=====")
        print(f"Welcome, {admin_name}")
        print("1. Create User")
        print("2. view Users")
        print("3. Update User")
        print("4. Deactive user")
        print("5. Logout")

        choice= input("Enter your choice (1-5):")
        if choice== "1":
            create_user()
        elif choice=="2":
            view_users()
        elif choice=="3":
            update_user()
        elif choice=="4":
            deactive_user()
        elif choice=="5":
            print("Loggin out...")
            break
        else:
            print("Invalid choice. Please try again.")

def create_user():
    full_name=input("Enter a full Username: ")
    username=input("Enter username: ")
    password=input("Enter password:")
    email=input("Enter email: ")
    phone=int(input("Enter phone number: "))
    gender=input("Enter gender: ")
    role=input("Enter role: ")
   

        



        
