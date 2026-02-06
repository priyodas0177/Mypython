# from flask import render_template, redirect, url_for, session

# def dashboard_routes(app):

#     def admin_required():
#         return session.get("user_type") == "admin"

#     @app.route("/admin/dashboard")
#     def admin_dashboard():
#         if not admin_required():
#             return redirect(url_for("login_page", expired=1))

#         return render_template(
#             "admin_dashboard.html",
#             admin_name=session.get("admin_name"),
#             admin_id=session.get("admin_id")
#         )

#     @app.route("/admin/users")
#     def admin_users_page():
#         if not admin_required():
#             return redirect(url_for("login_page", expired=1))

#         return render_template(
#             "admin_users.html",
#             admin_name=session.get("admin_name")
#         )
