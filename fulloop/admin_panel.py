
class AdminPanel:
    def __init__(self, admin_id, admin_name):
        self.admin_id = admin_id
        self.admin_name = admin_name

    def show_menu(self):
        while True:
            print("\n===== ADMIN PANEL =====")
            print(f"Welcome, {self.admin_id} - {self.admin_name}")
            print("1. Create User")
            print("2. View Admin Users")
            print("3. View Users")
            print("4. Update User")
            print("5. User Status")
            print("6. Delete User")
            print("7. Logout")

            choice = input("Enter your choice (1-7): ")

            if choice == "1":
                self.create_user()
            elif choice == "2":
                self.view_admin_users()
            elif choice == "3":
                self.view_users()
            elif choice == "4":
                self.update_user()
            elif choice == "5":
                self.user_status_menu()
            elif choice == "6":
                self.delete_user()
            elif choice == "7":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    #===== Admin Features =====

    # def create_user(self):
    #     print("Create user logic here")

    # def view_admin_users(self):
    #     print("View admin users logic here")

    # def view_users(self):
    #     print("View users logic here")

    # def update_user(self):
    #     print("Update user logic here")

    # def user_status_menu(self):
    #     print("User status logic here")

    # def delete_user(self):
    #     print(f"Deleting user by admin ID: {self.admin_id}")
