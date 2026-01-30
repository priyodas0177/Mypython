from database import get_connection


class ViewService:
    def __init__(self):
        pass

    def view_admin_users(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM admin")
        total_admin = cursor.fetchone()[0]

        cursor.execute("SELECT id, name, role, is_active FROM admin")
        admins = cursor.fetchall()

        print("\n--- Admin User List ---")
        print(f"Total Admin Users: {total_admin}")

        for a in admins:
            status = "Active" if a[3] == 1 else "Inactive"
            print(f"ID: {a[0]}, Name: {a[1]}, Role: {a[2]}, Status: {status}")

        cursor.close()
        conn.close()

    def view_users(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("""
            SELECT id, fullname, username, email, phone, gender, role, is_active
            FROM users
        """)
        users = cursor.fetchall()

        print("\n--- See All Users List ---")
        print(f"Total Users: {total_users}")

        for u in users:
            status = "Active" if u[7] == 1 else "Inactive"
            print(
                f"ID:{u[0]}, fullname:{u[1]}, username:{u[2]}, email:{u[3]}, "
                f"phone:{u[4]}, gender:{u[5]}, role:{u[6]}, status:{status}"
            )

        cursor.close()
        conn.close()
