how to multipe user login:
users = {
    "priyo": {
        "password": "pri123",
        "is_active": True
    },
    "rahim": {
        "password": "rahim456",
        "is_active": False
    },
    "karim": {
        "password": "karim789",
        "is_active": True
    }
}

username = input("Enter username: ").strip().lower()
password = input("Enter password: ").strip()

if username in users:
    if users[username]["password"] == password:
        if users[username]["is_active"]:
            print("Login successful ✅ Welcome", username)
        else:
            print("Account inactive ❌ Contact admin")
    else:
        print("Wrong password ❌")
else:
    print("User not found ❌")

next step: 
1.	🔒 Hide password while typing
	2.	🔁 Limit login attempts
