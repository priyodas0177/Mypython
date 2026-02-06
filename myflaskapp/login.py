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


# -------------- Admin Dashboard ------------------
@app.route("/dashboard")
def dashboard():
    if not session.get("user_type"):
        return redirect(url_for("login_page", expired=1))

    return render_template(
        "Dashboard.html",
        admin_name=session.get("admin_name"),
        user_name=session.get("user_name")
    )



@app.context_processor
def inject_permission():
    return dict(has_permission=has_permission)


# ------------------ Logout ------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


# ------------------ Run Server ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
