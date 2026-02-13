from datetime import datetime, time

LATE_TIME = time(9, 30)      # after 09:30 => late
END_TIME  = time(18, 0)      # before 18:00 => early leave


def log_login(conn, user_id):
    now = datetime.now()
    today = now.date()
    cursor = conn.cursor()

    # 1) save login event
    cursor.execute(
        "INSERT INTO attendance_events (user_id, event_type, event_time) VALUES (%s,'login',%s)",
        (user_id, now)
    )

    # 2) check daily row exists?
    cursor.execute(
        "SELECT id, in_time, remarks FROM attendance_daily WHERE user_id=%s AND att_date=%s",
        (user_id, today)
    )
    row = cursor.fetchone()

    if row is None:
        # first time today → create daily record
        remarks = "Late" if now.time() > LATE_TIME else ""
        cursor.execute("""
            INSERT INTO attendance_daily (user_id, att_date, in_time, status, remarks)
            VALUES (%s, %s, %s, 'present', %s)
        """, (user_id, today, now, remarks))
    else:
        # already created today → do nothing (keep first in_time)
        cursor.execute("""
            UPDATE attendance_daily SET status='present'
            WHERE user_id=%s AND att_date=%s
        """, (user_id, today))

    conn.commit()
    cursor.close()


def log_logout(conn, user_id):
    now = datetime.now()
    today = now.date()
    cursor = conn.cursor()

    # 1) save logout event
    cursor.execute(
        "INSERT INTO attendance_events (user_id, event_type, event_time) VALUES (%s,'logout',%s)",
        (user_id, now)
    )

    # 2) update daily row (out_time + stay_minutes + early leave)
    cursor.execute(
        "SELECT in_time, remarks FROM attendance_daily WHERE user_id=%s AND att_date=%s",
        (user_id, today)
    )
    row = cursor.fetchone()

    if row:
        in_time, old_remarks = row

        # stay time minutes
        stay_minutes = None
        if in_time:
            stay_minutes = int((now - in_time).total_seconds() / 60)

        # early leave?
        remarks = old_remarks or ""
        if now.time() < END_TIME:
            if remarks:
                remarks = remarks + ", Early Leave"
            else:
                remarks = "Early Leave"

        cursor.execute("""
            UPDATE attendance_daily
            SET out_time=%s, stay_minutes=%s, remarks=%s, status='present'
            WHERE user_id=%s AND att_date=%s
        """, (now, stay_minutes, remarks, user_id, today))

    conn.commit()
    cursor.close()
