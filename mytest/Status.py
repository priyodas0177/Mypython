from database import get_connection

def user_status_menu():
    while True:
        print("\nUSER STATUS MENU")
        print("1. Deactivate Admin")
        print("2. Reactivate Admin")
        print("3. Deactivate User")
        print("4. Reactivate User")
        print("5. Back")

        choice = input("Choose any one: ")
        if choice == "1":
            admin_id = int(input("Enter Admin ID: "))
            set_admin_status(admin_id, 0)
        elif choice == "2":
            admin_id = int(input("Enter Admin ID: "))
            set_admin_status(admin_id, 1)
        elif choice == "3":
            user_id = int(input("Enter User ID: "))
            set_user_status(user_id, 0)
        elif choice == "4":
            user_id = int(input("Enter User ID: "))
            set_user_status(user_id, 1)
        elif choice == "5":
            return  
        else:
            print("Invalid choice.")


def set_admin_status(admin_id, status):
    conn = get_connection()
    curser = conn.cursor()

    curser.execute("SELECT id FROM admin WHERE id=%s", (admin_id,))
    if not curser.fetchone():
        print(" Admin not found.")
        curser.close()
        conn.close()
        return

    curser.execute(
        "UPDATE admin SET is_active=%s WHERE id=%s",(status, admin_id))
    conn.commit()

    action = "Reactivated" if status == 1 else "Deactivated"
    print(f"...Admin {action} successfully...")

    curser.close()
    conn.close()


def set_user_status(user_id, status):
    conn = get_connection()
    curser = conn.cursor()

    curser.execute("SELECT id FROM users WHERE id=%s", (user_id,))
    if not curser.fetchone():
        print(" User not found.")
        curser.close()
        conn.close()
        return

    curser.execute(
        "UPDATE users SET is_active=%s WHERE id=%s",(status, user_id))
    conn.commit()

    action = "Reactivated" if status == 1 else "Deactivated"
    print(f"...User {action} successfully...")

    curser.close()
    conn.close()
