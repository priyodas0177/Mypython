class User_Panel:

    def __init__(self,user_id, username,role ):
        self.user_id=user_id
        self.username=username
        self.role=role
        
    def show_menu(self):
        print("Login Successfully... ")
        print(f"Welcome {self.username}({self.user_id})")
