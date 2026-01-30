from django.shortcuts import render, redirect
#from django.contrib.auth import authenticate, login
from django.db import connection

# Create your views here.
def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username", "").strip()
        password=request.POST.get("Password", "")

        with connection.cursor() as curser:
            curser.execute(
                """
                SELECT id, name FROM admin WHERE name=%s and password=%s 
                AND is_active=1
                """,
                [username,password]
                
            )
            result_admin=curser.fetchone()

            if result_admin:
                admin_id, admin_name=result_admin

                request.session("user_type")="admin"
                request.session("admin_id")=admin_id
                request.session("admin_name")=admin_name
                return redirect("admin_dashboard")



            curser.execute(
                """
                SELECT id, name, role from users WHERE username=%s AND password
                AND is_active=1 
                """
                [username,password]
            )
            result_user=curser.execute()

            if result_user:
                user_id, user_name, role=result_user

                request.session["user_type"]="user"
                request.session["user_id"]=user_id
                request.session["username"]=username
                request.session["role"]=role

                return redirect("user_dashboard")
            return render(request, "login.html", {"message":"Invalid Username and "
                "Passaword"})
        return render(request, "login.html")