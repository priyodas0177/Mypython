from database import get_connection

def verify_password(admin_id,password):
    conn=get_connection()
    curser=conn.cursor()

    curser.execute("""SELECT id FROM admin WHERE id=%s AND password=%s 
                   AND is_active=1""",(admin_id,password))
    result=curser.fetchone()

    curser.close()
    conn.close()

    return result is not None

def delete_user(admin_id):
    print("\n === DELETE CONFIRMATION ===")

    password=input("Enter Your Password: ")

    if not verify_password(admin_id,password):
        print("...Wrong Password...\n")
        return
    
    user_id=int(input("Enter User Id: "))
    conn=get_connection()
    curser=conn.cursor()

    curser.execute("SELECT id FROM users WHERE id=%s",(user_id,))
    if not curser.fetchone():
        print("*** User Not Found ***")
        curser.close()
        conn.close()
        return
    
    curser.execute("DELETE FROM users Where id=%s",(user_id,))
    conn.commit()

    curser.close()
    conn.close()
    print("... User delete successfully ...")