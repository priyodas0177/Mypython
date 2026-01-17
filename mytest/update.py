from database import get_connection

def update_user():
    while True:
        print("UPDATE MENU: ")
        print("1. Update Admin")
        print("2. Update User")
        print("3. Back")

        choice=input("Choose any one: ")
        if choice=="1":
            admin_update()
        elif choice=="2":
            user_update() 
        else:
            print("Invalid choice.")


        
def admin_update():
    admin_id=int(input("Enter admin id to update: "))
    new_name=input("Enter new name:")

    conn=get_connection()
    curser=conn.cursor()

    curser.execute("select id from admin where id=%s",(admin_id,))
    if not curser.fetchone():
        print("Admin id not found")
        curser.close()
        conn.close()
        return

    sql="""UPDATE admin SET name=%s Where id=%s"""
    curser.execute(sql,(new_name, admin_id))
    conn.commit()
    print("Admin update Successfully.")

    curser.close()
    conn.close()
    
def user_update():
    user_id=int(input("Enter user id to update: "))
    conn=get_connection()
    curser=conn.cursor()

    curser.execute("select id from users where id=%s",(user_id,))
    if not curser.fetchone():
        print("User not found. give a valid user id. ")
        curser.close()
        conn.close()
        return
    
    while True:
        print("---USER UPDATE MENU---")
        print("1. Update Uner FullName")
        print("2. Update Uner Username")
        print("3. Update Uner Psssword")
        print("4. Update Uner Email")
        print("5. Update Uner Phone Number")
        print("6. Update Uner Role")
        print("7. Back")

        choice=input("Choose any one: ")
        if choice=="1":
            new_fullname(user_id)
        elif choice=="2":
            new_username(user_id)
        elif choice=="3":
            new_password(user_id)
        elif choice=="4":
            new_email(user_id)
        elif choice=="5":
            new_phonenumber(user_id)
        elif choice=="6":
            new_role(user_id)
        else:
            print("Invalid choice. ")

def new_fullname(user_id):
    name=input("Enter new full name:")
    conn=get_connection()
    curser=conn.cursor()

    sql="UPDATE users set fullname=%s WHERE id=%s"
    curser.execute(sql,(name,user_id))
    conn.commit()
    print("...New Fullname Update Successfully... ")

    curser.close()
    conn.close()

def new_username(user_id):
    while True:
        name=input("Enter new full name: ")

        if is_user_exist(name):
            print("Username already exists. Please choose a different username.")
        else:
            conn=get_connection()
            curser=conn.cursor()
            
            sql="UPDATE users set username=%s WHERE id=%s"
            curser.execute(sql,(name,user_id))
            conn.commit()
            print("...Username Update Successfully... ")

            curser.close()
            conn.close()
            break

def new_password(user_id):
    password=input("Enter new Password:")
    conn=get_connection()
    curser=conn.cursor()

    sql="UPDATE users set password=%s where id=%s"
    curser.execute(sql,(password,user_id))
    conn.commit()
    print("...Password Update Successfully... ")

    curser.close()
    conn.close()

def new_email(user_id):
    while True:
        email=input("Enter new Email: ")

        if is_user_exist(email):
            print("Username already exists. Please choose a different username.")
        else:
            conn=get_connection()
            curser=conn.cursor()
            
            sql="UPDATE users set email=%s WHERE id=%s"
            curser.execute(sql,(email,user_id))
            conn.commit()
            print("...Email Update Successfully... ")

            curser.close()
            conn.close()
            break

def new_phonenumber(user_id):
    phone=input("Enter new Phone Number:")
    conn=get_connection()
    curser=conn.cursor()

    sql="UPDATE users set phone=%s where id=%s"
    curser.execute(sql,(phone,user_id))
    conn.commit()
    print("...New Phone Number Update Successfully... ")

    curser.close()
    conn.close()

def new_role(user_id):
    while True:
            print("--Select New Role:--")
            print("1. Admin")
            print("2. Employee")
            print("3. Manager")

            choice=int(input("Enter your Choice (1-3): "))
            if choice==1:
                role ="Admin"
            elif choice==2:
                role ="Employee"
            elif choice==3:
                role= "Manager"
            else:
                print("Invalid choice. please try again.")
                continue
    
            conn=get_connection()
            curser=conn.cursor()

            sql="UPDATE users set role=%s where id=%s"
            curser.execute(sql,(role,user_id))
            conn.commit()
            print("...New Role Update Successfully... ")

            curser.close()
            conn.close() 