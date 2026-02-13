from datetime import datetime, time
from flask import Flask, session, redirect, url_for
from all_details_user import has_permission



LATE_TIME = time(9, 30)        # after 09:30 => Late
ABSENT_AFTER = time(17, 0)     # after 17:00 => Absent
END_TIME = time(18, 0)         # before 18:00 => Early Leave


def log_login(conn, user_id):
    if not session.get("user_type"):
        return redirect(url_for("login_page", expired=1))

    if not (
        session.get("user_type") == "admin"
        or (has_permission("create_user") and has_permission("give_permission"))
    ):
        return redirect(url_for("dashboard"))

    
    cursor = conn.cursor()
    now = datetime.now() #current date and time
    today = now.date() # only today's date (YYYY-MM-DD)

    # 1) store login history in attendance_events columns
    cursor.execute(
        "INSERT INTO attendance_events (user_id, event_type, event_time) VALUES (%s, %s, %s)",
        (user_id, "login", now)
    )

    # 2) check if today's daily record already exists
    cursor.execute(
        "SELECT id FROM attendance_daily WHERE user_id=%s AND att_date=%s",
        (user_id, today)
    )
    row = cursor.fetchone()

    if row is None:
        # first login today, Absent if login after 5 PM
        if now.time() > ABSENT_AFTER:
            cursor.execute("""
                INSERT INTO attendance_daily (user_id, att_date, in_time, status, remarks)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, today, now, "Absent", "Login After 5PM"))
        else:
            remarks = "Late" if now.time() > LATE_TIME else "" #check if user late or not 
            cursor.execute(""" 
                INSERT INTO attendance_daily (user_id, att_date, in_time, status, remarks)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, today, now, "present", remarks)) #insert all data

    conn.commit()
    cursor.close()


def log_logout(conn, user_id):
    if not session.get("user_type"):
        return redirect(url_for("login_page", expired=1))

    if not (
        session.get("user_type") == "admin"
        or (has_permission("create_user") and has_permission("give_permission"))
    ):
        return redirect(url_for("dashboard"))
    
    
    cursor = conn.cursor()
    now = datetime.now()
    today = now.date()

    # 1) save logout history
    cursor.execute(
        "INSERT INTO attendance_events (user_id, event_type, event_time) VALUES (%s, %s, %s)",
        (user_id, "logout", now)
    )

    # 2) get today's daily recods
    cursor.execute("""
        SELECT in_time, remarks, status
        FROM attendance_daily
        WHERE user_id=%s AND att_date=%s
    """, (user_id, today))
    row = cursor.fetchone()

    
    if row:
        in_time = row[0]
        old_remarks = row[1] or ""
        status = (row[2] or "Absent").lower()

        # 3) calculate stay minutes
        stay_minutes = None
        if in_time:
            stay_minutes = int((now - in_time).total_seconds() // 60)

        # 4) Early leave check (only if present)
        remarks = old_remarks
        if status == "present" and now.time() < END_TIME:
            if "Early Leave" not in remarks:
                remarks = (remarks + ", " if remarks else "") + "Early Leave"

        # 5)  UPDATE daily table 
        cursor.execute("""
            UPDATE attendance_daily
            SET out_time=%s,
                stay_minutes=%s,
                remarks=%s
            WHERE user_id=%s AND att_date=%s
        """, (now, stay_minutes, remarks, user_id, today))

    conn.commit()
    cursor.close()
