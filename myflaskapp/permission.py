from flask import session, redirect, url_for
from database import get_connection

# ------------- Helper: Check Admin/User ------------------
def role_requered(role):
    return session.get("user_type") == role

#------------- Permission---------
def has_permission(feature_code):
    if session.get("user_type")=="admin":
        return True  #admin has all permission
    
    user_id=session.get("user_id")
    if not user_id:
        return False
    
    conn=get_connection()
    curser=conn.cursor()

    curser.execute("""
                   SELECT is_allowed FROM user_permissions WHERE 
                   user_id=%s AND feature_code=%s""",(user_id, feature_code) )
    result=curser.fetchone()
    curser.close()
    conn.close()
    if result is None:
        return False

    return result[0] == 1
