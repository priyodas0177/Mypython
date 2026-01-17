from database import get_connection

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