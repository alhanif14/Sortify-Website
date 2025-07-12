from fasthtml.common import *
from function.scan import scan_section, scan_result_section, scan1_section, scan_logged_section
from database.database import get_db_session
from database.models import User, WasteDetectionLog
from fastapi.responses import RedirectResponse, JSONResponse
from datetime import datetime
from fastapi import Request

def scan_routes(rt):
    @rt("/scan1")
    def scan1(request: Request):
        return scan1_section()

    @rt("/scan")
    def scan(request: Request):
        # Check if user is logged in
        user_id = request.session.get("user_id")
        
        if not user_id:
            return RedirectResponse(url="/scan1", status_code=302)
        
        db = get_db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return RedirectResponse(url="/login", status_code=302)
            
            return scan_logged_section(user)
        finally:
            db.close()
    
    @rt("/scan_result")
    def scan_result(request: Request):
        # Get scan parameters
        waste_type = request.query_params.get("waste_type", "")
        point = request.query_params.get("point", "0")
        timestamp = request.query_params.get("timestamp", None)
        dispose_id = request.query_params.get("id", None)
        
        print(f"Scan result params - waste_type: {waste_type}, point: {point}, timestamp: {timestamp}, id: {dispose_id}")
        
        user_id = request.session.get("user_id")
        user = None
        
        if user_id:
            db = get_db_session()
            try:
                user = db.query(User).filter(User.id == user_id).first()
                
                if user:
                    points_to_add = int(point) if point.isdigit() else 0
                    if points_to_add > 0:
                        if user.point is None:
                            user.point = 0
                        user.point += points_to_add
                        db.commit()
                        print(f"✅ Added {points_to_add} points to user {user.username}. Total: {user.point}")
            except Exception as e:
                print(f"❌ Error updating user points: {e}")
                db.rollback()
            finally:
                db.close()
        
        return scan_result_section(request, user)

    @rt("/process_scan")
    def process_scan(request: Request):
        user_id = request.session.get("user_id")

        if not user_id:
            return JSONResponse({"status": "error", "message": "User not logged in"}, status_code=401)

        waste_type = request.query_params.get("waste_type", "")
        point = request.query_params.get("point", "0")
        timestamp = request.query_params.get("timestamp", "")
        dispose_id = request.query_params.get("id", "")

        print(f"Process Scan - waste_type: {waste_type}, point: {point}, timestamp: {timestamp}, id: {dispose_id}")

        db = get_db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return JSONResponse({"status": "error", "message": "User not found"}, status_code=404)

            points_to_add = int(point) if point.isdigit() else 0

            if points_to_add > 0:
                if user.point is None:
                    user.point = 0
                user.point += points_to_add

                # UPDATE log, not INSERT
                log = db.query(WasteDetectionLog).filter(WasteDetectionLog.id == dispose_id).first()
                if log:
                    log.username = user.username
                    print(f"📝 Updated WasteDetectionLog ID {dispose_id} with username: {user.username}")
                else:
                    print(f"⚠️ WasteDetectionLog with ID {dispose_id} not found.")

                db.commit()
                print(f"✅ User {user.username} points updated.")

            return JSONResponse({
                "status": "ok",
                "waste_type": waste_type,
                "point": point,
                "timestamp": timestamp,
                "id": dispose_id
            })

        except Exception as e:
            db.rollback()
            print(f"❌ Error: {e}")
            return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
        finally:
            db.close()