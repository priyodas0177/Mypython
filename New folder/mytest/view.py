from database import get_connection


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
