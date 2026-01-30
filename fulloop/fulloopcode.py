
import mysql.connector

# ------------------- DATABASE -------------------
class Database:
    def __init__(self, host='localhost', user='root', password='', database='testdb'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

# ------------------- USER CLASS -------------------
class User:
    def __init__(self, db: Database):
        self.db = db

    # ----- VALIDATIONS -----
    @staticmethod
    def get_phone():
        while True:
            phone = input("Enter phone number: ")
            if not phone.isdigit() or len(phone) != 11:
                print("Phone number must be exactly 11 digits.\n")
            else:
                return phone

    @staticmethod
    def get_gender():
        while True:
            print("Select Gender:\n1. Male\n2. Female\n3. Others")
            choice = input("Enter choice (1-3): ")
            if choice == "1":
                return "Male"
            elif choice == "2":
                return "Female"
            elif choice == "3":
                return "Others"
            else:
                print("Invalid choice. Try again.\n")

    @staticmethod
    def get_role():
        while True:
            print("Select Role:\n1. Admin\n2. Employee\n3. Manager")
            choice = input("Enter choice (1-3): ")
            if choice == "1":
                return "Admin"
            elif choice == "2":
                return "Employee"
            elif choice == "3":
                return "Manager"
            else:
                print("Invalid choice. Try again.\n")

    # ----- CHECK IF EXISTS -----
    def is_user_exist(self, username):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    def is_email_exist(self, email):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    # ----- UNIQUE INPUTS -----
    def get_unique_username(self):
        while True:
            uname = input("Enter Username: ")
            if self.is_user_exist(uname):
                print("Username already exists. Try again.\n")
            else:
                return uname

    def get_unique_email(self):
        while True:
            email = input("Enter Email: ")
            if self.is_email_exist(email):
                print("Email already exists. Try again.\n")
            else:
                return email

    # ----- CRUD OPERATIONS -----
    def create_user(self):
        fullname = input("Enter full name: ")
        username = self.get_unique_username()
        password = input("Enter password: ")
        email = self.get_unique_email()
        phone = self.get_phone()
        gender = self.get_gender()
        role = self.get_role()

        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO users (fullname, username, password, email, phone, gender, role, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
        """
        cursor.execute(sql, (fullname, username, password, email, phone, gender, role))
        conn.commit()
        cursor.close()
        conn.close()
        print("User created successfully.\n")

    def view_users(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, fullname, username, email, phone, gender, role, is_active FROM users")
        users = cursor.fetchall()
        print("\n--- Users List ---")
        for u in users:
            status = "Active" if u[7] == 1 else "Inactive"
            print(f"ID:{u[0]}, Name:{u[1]}, Username:{u[2]}, Email:{u[3]}, Phone:{u[4]}, Gender:{u[5]}, Role:{u[6]}, Status:{status}")
        cursor.close()
        conn.close()

    def set_user_status(self, user_id, status):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id=%s", (user_id,))
        if not cursor.fetchone():
            print("User not found.")
        else:
            cursor.execute("UPDATE users SET is_active=%s WHERE id=%s", (status, user_id))
            conn.commit()
            action = "Activated" if status == 1 else "Deactivated"
            print(f"User {action} successfully.")
        cursor.close()
        conn.close()

    def update_user(self, user_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id=%s", (user_id,))
        if not cursor.fetchone():
            print("*** User not found ***")
            cursor.close()
            conn.close()
            return
        cursor.close()
        conn.close()

        while True:
            print("\n--- USER UPDATE MENU ---")
            print("1. Full Name\n2. Username\n3. Password\n4. Email\n5. Phone\n6. Role\n7. Back")
            choice = input("Enter choice: ")
            if choice == "1":
                name = input("Enter new full name: ")
                self.execute_update(user_id, "fullname", name)
            elif choice == "2":
                while True:
                    uname = input("Enter new username: ")
                    if self.is_user_exist(uname):
                        print("Username exists, try another.")
                    else:
                        self.execute_update(user_id, "username", uname)
                        break
            elif choice == "3":
                pwd = input("Enter new password: ")
                self.execute_update(user_id, "password", pwd)
            elif choice == "4":
                while True:
                    email = input("Enter new email: ")
                    if self.is_email_exist(email):
                        print("Email exists, try another.")
                    else:
                        self.execute_update(user_id, "email", email)
                        break
            elif choice == "5":
                phone = self.get_phone()
                self.execute_update(user_id, "phone", phone)
            elif choice == "6":
                role = self.get_role()
                self.execute_update(user_id, "role", role)
            elif choice == "7":
                break
            else:
                print("Invalid choice.")

    def execute_update(self, user_id, field, value):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET {field}=%s WHERE id=%s", (value, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"{field} updated successfully.")

    def delete_user(self, user_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id=%s", (user_id,))
        if not cursor.fetchone():
            print("User not found.")
            cursor.close()
            conn.close()
            return
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("User deleted successfully.")

# ------------------- ADMIN CLASS -------------------
class Admin:
    def __init__(self, db: Database):
        self.db = db
        self.user_obj = User(db)

    def verify_password(self, admin_id, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM admin WHERE id=%s AND password=%s AND is_active=1", (admin_id, password))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None

    def view_admin_users(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, role, is_active FROM admin")
        admins = cursor.fetchall()
        print("\n--- Admin Users ---")
        for a in admins:
            status = "Active" if a[3] == 1 else "Inactive"
            print(f"ID:{a[0]}, Name:{a[1]}, Role:{a[2]}, Status:{status}")
        cursor.close()
        conn.close()

    def update_admin(self, admin_id):
        new_name = input("Enter new admin name: ")
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE admin SET name=%s WHERE id=%s", (new_name, admin_id))
        conn.commit()
        cursor.close()
        conn.close()
        print("Admin updated successfully.")

    def set_admin_status(self, admin_id, status):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM admin WHERE id=%s", (admin_id,))
        if not cursor.fetchone():
            print("Admin not found.")
        else:
            cursor.execute("UPDATE admin SET is_active=%s WHERE id=%s", (status, admin_id))
            conn.commit()
            action = "Activated" if status == 1 else "Deactivated"
            print(f"Admin {action} successfully.")
        cursor.close()
        conn.close()

    # ----- ADMIN PANEL -----
    def admin_panel(self, admin_id, admin_name):
        while True:
            print(f"\n=== ADMIN PANEL ===\nWelcome {admin_name}")
            print("1. Create User\n2. View Admin Users\n3. View Users\n4. Update Admin\n5. Update User\n6. User/Admin Status\n7. Delete User\n8. Logout")
            choice = input("Enter choice (1-8): ")
            if choice == "1":
                self.user_obj.create_user()
            elif choice == "2":
                self.view_admin_users()
            elif choice == "3":
                self.user_obj.view_users()
            elif choice == "4":
                self.update_admin(admin_id)
            elif choice == "5":
                uid = int(input("Enter User ID to update: "))
                self.user_obj.update_user(uid)
            elif choice == "6":
                self.user_status_menu()
            elif choice == "7":
                uid = int(input("Enter User ID to delete: "))
                pwd = input("Enter your password: ")
                if self.verify_password(admin_id, pwd):
                    self.user_obj.delete_user(uid)
                else:
                    print("Wrong password. Cannot delete user.")
            elif choice == "8":
                print("Logging out...")
                break
            else:
                print("Invalid choice.")

    # ----- USER/ADMIN STATUS MENU -----
    def user_status_menu(self):
        while True:
            print("\n--- STATUS MENU ---")
            print("1. Deactivate Admin\n2. Activate Admin\n3. Deactivate User\n4. Activate User\n5. Back")
            choice = input("Enter choice: ")
            if choice == "1":
                aid = int(input("Enter Admin ID: "))
                self.set_admin_status(aid, 0)
            elif choice == "2":
                aid = int(input("Enter Admin ID: "))
                self.set_admin_status(aid, 1)
            elif choice == "3":
                uid = int(input("Enter User ID: "))
                self.user_obj.set_user_status(uid, 0)
            elif choice == "4":
                uid = int(input("Enter User ID: "))
                self.user_obj.set_user_status(uid, 1)
            elif choice == "5":
                break
            else:
                print("Invalid choice.")

    # ----- LOGIN -----
    def login(self):
        username = input("Enter admin username: ")
        password = input("Enter password: ")
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM admin WHERE name=%s AND password=%s AND is_active=1", (username, password))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            admin_id, admin_name = result
            print(f"\nWelcome Admin: {admin_name}")
            self.admin_panel(admin_id, admin_name)
        else:
            print("Invalid credentials.")

# ------------------- MAIN -------------------
if __name__ == "__main__":
    db = Database(host="localhost", user="root", password="@H.dpriyo0177@.", database="testdb")
    admin = Admin(db)
    admin.login()