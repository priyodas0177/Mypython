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


# def init_user_update_routes(app):
#     @app.route("/admin/update_user/<int:user_id>",methods=["GET","POST"])
#     def update_user(user_id):

#         error=None
#         success=None

#         conn=get_connection()
#         curser=conn.cursor()

#         curser.execute("""SELECT id, fullname, username, password, email, phone,
#                     gender, role FROM users WHERE id=%s""",(user_id,))
        
#         result_user=curser.fetchone()

#         if not result_user:
#             curser.close()
#             conn.close()
#             return "User not found."
        
#         old_fullname=result_user[1]
#         old_username=result_user[2]
#         old_password=result_user[3]
#         old_email=result_user[4]
#         old_phone=result_user[5]
#         old_gender=result_user[6]
#         old_role=result_user[7]

#         if request.method=="POST":
#             fullname=request.form.get("fullname","").strip()
#             username=request.form.get("username","").strip()
#             password=request.form.get("password","").strip()
#             email=request.form.get("email","").strip()
#             phone=request.form.get("phone","").strip()
#             gender=request.form.get("gender","").strip()
#             role=request.form.get("role","").strip()

#             #if input empty keep old data
#             fullname=fullname if fullname else old_fullname
#             username=username if username else old_username
#             password=password if password else old_password
#             email=email if email else old_email
#             phone=phone if phone else old_phone
#             gender=gender if gender else old_gender
#             role=role if role else old_role

#             #password: only update if user type new password 
#             final_password=password if password else old_password

#             #validation after filling defaulti
#             if not fullname or not username or not email:
#                 error="fullname, usernname, email cannot be empty."

#             elif phone and ((not phone.isdigit()) or (len(phone)!=11)):
#                 error="Invalid phone number. Must be 11 digit number."

#             elif gender not in ["Male","Female","Others"]:
#                 error="Invalid Gender."

#             elif role not in ["Admin", "Employee", "Manager", "HR"]:
#                 error="Invalid Role."
#             else:
#                 curser.execute("""
#                     UPDATE users
#                     SET fullname=%s, username=%s, password=%s,
#                         email=%s, phone=%s, gender=%s, role=%s
#                     WHERE id=%s""", 
#                     (fullname, username, final_password, email, phone, gender, role, user_id))

#                 conn.commit()
#                 success="User Update Successfully."


#             # curser.execute("""SELECT id, fullname, username, password, email, phone,
#             #         gender, role FROM users WHERE id=%s""",(user_id,))
#             # result_user=curser.fetchone()

#         curser.close()
#         conn.close()
#         return render_template("update_user.html", result_user=result_user, error=error, success=success)

from flask import render_template, request, redirect, url_for, session
from database import get_connection
from permission import has_permission  # if you use this

def init_user_update_routes(app):

    @app.route("/admin/update_user", methods=["GET", "POST"])
    def update_user():
        # --- security (edit as your project uses) ---
        if session.get("user_type") != "admin":
            return redirect(url_for("login_page", expired=1))
        # optional permission check
        if not (session.get("user_type") == "admin" or has_permission("update_user")):
            return redirect(url_for("dashboard"))

        error = None
        success = None
        result_user = None

        # Step-1: user_id can come from GET (?user_id=) or POST (hidden input)
        user_id = (request.args.get("user_id") or "").strip()
        if request.method == "POST":
            user_id = (request.form.get("user_id") or "").strip()

        # If no user_id yet -> just show search box
        if not user_id:
            return render_template("update_user.html", result_user=None, error=None, success=None)

        if not user_id.isdigit():
            return render_template("update_user.html", result_user=None,
                                   error="Please enter a valid numeric user id.", success=None)

        user_id = int(user_id)

        conn = get_connection()
        curser = conn.cursor()

        # Load user
        curser.execute("""
            SELECT id, fullname, username, password, email, phone, gender, role
            FROM users WHERE id=%s
        """, (user_id,))
        result_user = curser.fetchone()

        if not result_user:
            curser.close()
            conn.close()
            return render_template("update_user.html", result_user=None,
                                   error="User not found.", success=None)

        old_fullname = result_user[1]
        old_username = result_user[2]
        old_password = result_user[3]
        old_email    = result_user[4]
        old_phone    = result_user[5]
        old_gender   = result_user[6]
        old_role     = result_user[7]

        # Step-2: If POST -> update
        if request.method == "POST":
            fullname = request.form.get("fullname", "").strip() or old_fullname
            username = request.form.get("username", "").strip() or old_username
            password = request.form.get("password", "").strip()  # may be empty
            email    = request.form.get("email", "").strip() or old_email
            phone    = request.form.get("phone", "").strip() or old_phone
            gender   = request.form.get("gender", "").strip() or old_gender
            role     = request.form.get("role", "").strip() or old_role

            final_password = password if password else old_password

            if not fullname or not username or not email:
                error = "fullname, username, email cannot be empty."
            elif phone and ((not phone.isdigit()) or (len(phone) != 11)):
                error = "Invalid phone number. Must be 11 digit number."
            elif gender not in ["Male", "Female", "Others"]:
                error = "Invalid Gender."
            elif role not in ["Admin", "Employee", "Manager", "HR"]:
                error = "Invalid Role."
            else:
                curser.execute("""
                    UPDATE users
                    SET fullname=%s, username=%s, password=%s,
                        email=%s, phone=%s, gender=%s, role=%s
                    WHERE id=%s
                """, (fullname, username, final_password, email, phone, gender, role, user_id))
                conn.commit()
                success = "User Updated Successfully."

                # reload updated user
                curser.execute("""
                    SELECT id, fullname, username, password, email, phone, gender, role
                    FROM users WHERE id=%s
                """, (user_id,))
                result_user = curser.fetchone()

        curser.close()
        conn.close()

        return render_template("update_user.html", result_user=result_user, error=error, success=success)



