from database import get_connection
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session
from permission import has_permission, role_requered



app = Flask(__name__)
app.secret_key = "abcd"
app.permanent_session_lifetime = timedelta(minutes=15)


# ------------------ Home ------------------
@app.route("/")
def home():
    return redirect(url_for("login_page"))



# ------------------ Login ------------------
@app.route("/login", methods=["GET", "POST"])
def login_page():
    message = None
    session.clear()

    # show session expired message
    if request.args.get("expired") == "1":
        message = "Session expired. Please login again."

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_connection()
        cursor = conn.cursor()

#----------- Try admin ----------#
        cursor.execute("""
            SELECT id, name FROM admin
            WHERE name=%s AND password=%s AND is_active=1
        """, (username, password))

        result_admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if result_admin:
            admin_id, admin_name = result_admin

            session.clear()
            session.permanent = True
            session["user_type"] = "admin"
            session["admin_id"] = admin_id
            session["admin_name"] = admin_name

            return redirect(url_for("dashboard"))
        
#----------- Try Users ----------#
        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("""
            SELECT id, username, role from users Where username=%s AND 
                password=%s AND  is_active=1
        """, (username, password))
        result_user=cursor.fetchone()
        cursor.close()
        conn.close()

        if result_user:
            user_id, user_name, role=result_user

            session.clear()
            session.permanent=True
            session["user_type"]="user"
            session["user_id"]=user_id
            session["user_name"]=user_name
            session["role"]=role
            return redirect(url_for("dashboard"))

        return render_template("login.html", message="Invalid username or password")

    return render_template("login.html", message=message)

#---------------Display name -------------
def get_dispaly_name():
     return session.get("admin_name") or session.get("user_name") or "User"



# -------------- Admin Dashboard ------------------
@app.route("/dashboard")
def dashboard():
    if not session.get("user_type"):
        return redirect(url_for("login_page", expired=1))
    
    
    return render_template(
        "Dashboard.html",
        display_name=get_dispaly_name()
    )


@app.context_processor
def inject_permission():
    return dict(has_permission=has_permission)

#------------- Search User -------------
@app.route("/admin/search-user", methods=["GET", "POST"])
def search_user():
    if session.get("user_type") != "admin":
        return redirect(url_for("login_page", expired=1)) #expired=1 to show session expired message

    user = None
    error = None
    features = []
    allowed_map = {}
    
        
    conn = get_connection()
    cursor = conn.cursor()

    # � Load all features (ALWAYS)
    cursor.execute("SELECT feature_code, feature_name FROM features") #load all features to display in checkbox list
    features = cursor.fetchall()

    if request.method == "POST":
        user_id = request.form.get("user_id").strip() #get user id from input

        cursor.execute(
            "SELECT id, username, email FROM users WHERE id=%s",
            (user_id,)
        )
        user = cursor.fetchone()

        if not user:
            error = "User not found. please enter valid user id."
        else:
            cursor.execute("""
                SELECT feature_code, is_allowed
                FROM user_permissions
                WHERE user_id=%s
            """, (user[0],))

            allowed_map = {
                code: is_allowed for code, is_allowed in cursor.fetchall() # convert the db into a dictionary.
            }

    cursor.close()
    conn.close()
    
    
    return render_template(
        "search_user.html",
        user=user,
        error=error,
        features=features,
        allowed_map=allowed_map,
        display_name=get_dispaly_name()
    )


#------------- Save Permissions -------------
@app.route("/admin/save-permissions/<int:user_id>", methods=["POST"])
def save_permissions(user_id):
    if session.get("user_type") != "admin":
        return redirect(url_for("login_page", expired=1))

    selected = request.form.getlist("feature_codes")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # reset permissions
        cursor.execute(
            "UPDATE user_permissions SET is_allowed=0 WHERE user_id=%s", #reset all permissions that is selected before (permisssion back )
            (user_id,)
        )

        for code in selected:   #update the selected permissions TO 1 (permission allow)
            cursor.execute("""
                UPDATE user_permissions
                SET is_allowed=1
                WHERE user_id=%s AND feature_code=%s
            """, (user_id, code))

            if cursor.rowcount == 0: #it update the permission(insert data)
                cursor.execute("""
                    INSERT INTO user_permissions (user_id, feature_code, is_allowed) 
                    VALUES (%s, %s, 1)
                """, (user_id, code))

        conn.commit()

    except:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("search_user",user_id=user_id))




# ------------------ Logout ------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


# ------------------ Run Server ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
