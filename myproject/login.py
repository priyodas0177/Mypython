from database import get_connection
from flask import Flask, render_template,request,redirect,url_for,session

app=Flask(__name__)
app.secret_key="abcd"

@app.route("/")
def home():
    return redirect(url_for("login_page"))

@app.route("/login",methods=["GET","POST"])
def login_page():
     if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_connection()
        cursor = conn.cursor()

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
            session["user_type"] = "admin"
            session["admin_id"] = admin_id
            session["admin_name"] = admin_name

            return redirect(url_for("admin_dashboard"))
        
        return render_template("login.html", message="Invalid username or password")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)