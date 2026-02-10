from flask import render_template, redirect, url_for, request,session
from database import get_connection
from permission import has_permission

def is_user_exist(var_username):
    conn=get_connection()
    curser=conn.cursor()

    curser.execute("SELECT id FROM users WHERE username=%s",(var_username,))
    username_result=curser.fetchone()
    curser.close()
    conn.close()
    return username_result is not None

def is_email_exist(var_email):
    conn=get_connection()
    curser=conn.cursor()

    curser.execute("SELECT id FROM users WHERE email=%s",(var_email,))
    email_result=curser.fetchone()
    curser.close()
    conn.close()
    return email_result is not None


def init_user_create_routes(app):
    @app.route("/admin/create_user",methods=["GET","POST"])
    def create_user():
        
        error=None
        success=None

        if request.method=="POST":
            fullname=request.form.get("fullname", "").strip()
            username=request.form.get("username", "").strip()
            password=request.form.get("password", "").strip()
            email=request.form.get("email", "").strip()
            phone=request.form.get("phone", "").strip()
            gender=request.form.get("gender", "")
            role=request.form.get("role", "")

#----------- VALIDATION ---------------
            #if (not fullname) or (not username) or (not password) or (not email) or (not phone) or 
            # (not gender) or (not role):
            
            if not fullname or not username or not password or not email:
                error="please fill all the fields."
            elif is_user_exist(username):
                error="Username already exist. please choose a different username."
            elif is_email_exist(email):
                error="Email already exist. please choose a different email."
            elif (not phone.isdigit()) or (len(phone)!=11):
                error="Invalid phone number. please enter a valid 11-digit phone number."
            elif gender not in ["Male","Female","Others"]:
                error="Invalid Gender."
            elif role not in ["Admin","Employee","Manager","HR"]:
                error="Invalid Role."
            else:
                conn=get_connection()
                curser=conn.cursor()

                curser.execute("""INSERT INTO users (fullname, username, password, email,
                            phone, gender, role, is_active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                            (fullname, username, password, email, phone, gender, role, 1))
                conn.commit()
                curser.close()
                conn.close()
                success="User Created Successfully."

                return render_template("create_user.html", error=error,
                                    success=success)
            
        return render_template(
        "create_user.html",
        error=error,
        success=success,)

