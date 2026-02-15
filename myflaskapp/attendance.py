from datetime import datetime, time
from flask import Flask, session, redirect, url_for
from all_details_user import has_permission
from datetime import datetime, time

LATE_TIME = time(9, 30)        # after 09:30 => Late
ABSENT_AFTER = time(17, 0)     # after 17:00 => Absent
END_TIME = time(18, 0)         # before 18:00 => Early Leave


def get_dispaly_name():
    return session.get("admin_name") or session.get("user_name") or "User"

def log_login(conn, user_id):
    
    cursor = conn.cursor()
    now = datetime.now()
    today = now.date()
    display_name=get_dispaly_name()

    # 1) store login event
    cursor.execute(
        "INSERT INTO attendance_events (user_id, event_type, event_time) VALUES (%s, %s, %s)",
        (user_id, "login", now)
    )

    # 2) daily record exists?
    cursor.execute(
        "SELECT id FROM attendance_daily WHERE user_id=%s AND att_date=%s",
        (user_id, today)
    )
    row = cursor.fetchone()

    if row is None:
        if now.time() > ABSENT_AFTER:
            cursor.execute("""
                INSERT INTO attendance_daily (user_id, att_date, in_time, status, remarks)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, today, now, "Absent", "Login After 5PM"))
        else:
            remarks = "Late" if now.time() > LATE_TIME else ""
            cursor.execute("""
                INSERT INTO attendance_daily (user_id, att_date, in_time, status, remarks)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, today, now, "Present", remarks))

    conn.commit()
    cursor.close()


def log_logout(conn, user_id):
    cursor = conn.cursor()
    now = datetime.now()
    today = now.date()

    # 1) store logout event
    cursor.execute(
        "INSERT INTO attendance_events (user_id, event_type, event_time) VALUES (%s, %s, %s)",
        (user_id, "logout", now)
    )

    # 2) get today's daily record
    cursor.execute("""
        SELECT in_time, remarks, status
        FROM attendance_daily
        WHERE user_id=%s AND att_date=%s
    """, (user_id, today))
    row = cursor.fetchone()

    if row:
        in_time = row[0]
        old_remarks = row[1] or ""
        status = (row[2] or "").lower()

        stay_minutes = None
        if in_time:
            stay_minutes = int((now - in_time).total_seconds() // 60)

        remarks = old_remarks
        if status == "present" and now.time() < END_TIME:
            if "Early Leave" not in remarks:
                remarks = (remarks + ", " if remarks else "") + "Early Leave"

        cursor.execute("""
            UPDATE attendance_daily
            SET out_time=%s, stay_minutes=%s, remarks=%s
            WHERE user_id=%s AND att_date=%s
        """, (now, stay_minutes, remarks, user_id, today))

    conn.commit()
    cursor.close()

