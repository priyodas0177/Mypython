from database import get_connection

def admin_func(admin_id, admin_name):
    while True:
        print(f"\n=====ADMIN PANEL=====")
        print(f"Welcome, {admin_id,admin_name}")
        print("1. Create User")
        print("2. View Admin Users")
        print("3. view Users")
        print("4. Update User")
        print("5. Deactive user")
        print("6. Logout")

        choice= input("Enter your choice (1-5):")
        if choice== "1":
            create_user()
        elif choice=="2":
            view_admin_users()
        elif choice=="3":
            view_users()
        elif choice=="4":
            update_user()
        # elif choice=="4":
        #     deactive_user()
        # elif choice=="5":
        #     print("Loggin out...")
        #     break
        else:
            print("Invalid choice. Please try again.")


def is_email_exist(var_email):
    conn=get_connection()
    curser=conn.cursor()

    sql="SELECT id FROM users WHERE email=%s "
    curser.execute (sql, (var_email,))
    result=curser.fetchone()

    curser.close()
    conn.close()

    return result is not None

def get_unique_email():
    while True:
        email=input("Enter Email Address: ")

        if is_email_exist(email):
            print("email already exist. please try again. \n")
        else:
            return email

def is_user_exist(var_username):
    conn=get_connection()
    curser=conn.cursor()

    sql="SELECT id FROM users WHERE username=%s "
    curser.execute (sql, (var_username,))
    result=curser.fetchone()

    curser.close()
    conn.close()

    return result is not None

def get_unique_username():
    while True:
        uname=input("Enter Username: ")

        if is_user_exist(uname):
            print("username already exist. please try again. \n")
        else:
            return uname

def get_phone():
    while True:
        phone=input("Enter phone number: ")
        
        if not phone.isdigit():
            print("phone nunber must be contain 11 digit. \n")
            continue

        if len(phone)!=11:
            print("phone nunber must be exactle 11 digit. \n")
            continue
        return phone

def get_gender():
        while True:
            print("Select Gender:")
            print("1. Male")
            print("2. Female")
            print("3. Others")

            choice=int(input("Enter your choicre (1-3): "))
            if choice==1:
                return "Male"
            elif choice==2:
                return "Female"
            elif choice==3:
                return "Others"
            else:
                print("Invalid choice. Please try again. ")
               
def get_role():
        while True:
            print("Select Role:")
            print("1. Admin")
            print("2. Employee")
            print("3. Manager")

            choice=int(input("Enter your Choice (1-3): "))
            if choice==1:
                return "Admin"
            elif choice==2:
                return "Employee"
            elif choice==3:
                return "Manager"
            else:
                print("Invalid choice. please try again.")

def create_user():
    full_name=input("Enter a full Username: ")
    var_username=get_unique_username()
    #var_username=input("Enter username: ") #unique 
    password=input("Enter password:")
    var_email=get_unique_email()
    #email=input("Enter email: ")
    phone=get_phone()
    #phone=int(input("Enter phone number: ")) #work 11 digit only. 
    #gender=input("Enter gender: ")
    gender=get_gender()
    #role=input("Enter role: ")
    role=get_role()

    conn=get_connection()
    curser=conn.cursor()

    sql="""INSERT INTO users (fullname, username, password, email, phone, gender, role, is_active)
    VALUES (%s, %s,%s,%s,%s,%s,%s,%s)
    """

    curser.execute(sql, (full_name, var_username, password, var_email, phone, gender, role, 1))
    conn.commit()

    curser.close()
    conn.close()

    print("Users created Successfully. ")

def view_admin_users():

    conn = get_connection()
    curser = conn.cursor()

    curser.execute("select count(*) from admin ")
    total_users= curser.fetchone()[0]

    curser.execute("SELECT id, name, role, is_active FROM admin")
    users = curser.fetchall()

    print("\n--- User List ---")
    print(f"Total Admin Users:{total_users}")

    for u in users:    
        if u[3]==1:
            status="Active"
        else:
            status="Inavtive"
        print(f"ID: {u[0]}, Name: {u[1]}, Role: {u[2]}, Status: {status}")

    curser.close()
    conn.close()

def view_users():
    conn=get_connection()
    curser=conn.cursor()
    
    curser.execute("select count(*) from users")
    total_users=curser.fetchone()[0]

    curser.execute("select id, fullname, username, email, phone, gender,role, is_active from users")
    users=curser.fetchall()

    print("\n--- See All Users List ---")
    print(f"Totall Users: {total_users}")

    for u in users:
        status="Active" if u[7]==1 else "Inactive"
        print(f"""ID:{u[0]}, fullname:{u[1]}, username:{u[2]}, email:{u[3]}, phone:{u[4]},
              gender:{u[5]}, role:{u[6]}, is_active:{status}""")
    
    curser.close()
    conn.close()

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
    print("User update function called.")   



    

 
    

        



        
