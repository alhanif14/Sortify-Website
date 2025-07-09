from fasthtml.common import *
from function.scan import scan_section, scan_result_section, scan1_section, scan_logged_section
from database.database import get_db_session
from database.models import User

def scan_routes(rt):
    @rt("/scan1")
    def scan1():
        return scan1_section()

    @rt("/scan")
    def scan(request):
        # ✅ Check if user is logged in
        user_id = request.session.get("user_id")
        
        if not user_id:
            # ✅ If not logged in, redirect to scan1 (login prompt)
            return RedirectResponse(url="/scan1", status_code=302)
        
        # ✅ Get user data from database
        db = get_db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                # ✅ If user not found, redirect to login
                return RedirectResponse(url="/login", status_code=302)
            
            # ✅ Return scan page with user info
            return scan_logged_section(user)
        finally:
            db.close()
    
    @rt("/scan_result")
    def scan_result(request):
        # ✅ Get scan parameters
        waste_type = request.query_params.get("waste_type", "")
        point = request.query_params.get("point", "0")
        timestamp = request.query_params.get("timestamp", None)
        dispose_id = request.query_params.get("id", None)
        
        # ✅ Check if user is logged in
        user_id = request.session.get("user_id")
        user = None
        
        if user_id:
            db = get_db_session()
            try:
                user = db.query(User).filter(User.id == user_id).first()
                
                if user:
                    # ✅ ADD POINTS TO USER ACCOUNT HERE
                    points_to_add = int(point) if point.isdigit() else 0
                    if points_to_add > 0:
                        # Initialize point if None
                        if user.point is None:
                            user.point = 0
                        
                        # Add new points to existing points
                        user.point += points_to_add
                        
                        # Save to database
                        db.commit()
                        print(f"✅ Added {points_to_add} points to user {user.username}. Total: {user.point}")
                
            except Exception as e:
                print(f"❌ Error updating user points: {e}")
                db.rollback()
            finally:
                db.close()
        
        return scan_result_section(request, user)

    @rt("/process_scan")
    def process_scan(request):
        """Process scan result and add points before showing result"""
        user_id = request.session.get("user_id")
        
        if not user_id:
            return {"status": "error", "message": "User not logged in"}
        
        # Get parameters from request
        waste_type = request.query_params.get("waste_type", "")
        point = request.query_params.get("point", "0")
        timestamp = request.query_params.get("timestamp", "")
        dispose_id = request.query_params.get("id", "")
        
        db = get_db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"status": "error", "message": "User not found"}
            
            # ✅ Update user points
            points_to_add = int(point) if point.isdigit() else 0
            
            if points_to_add > 0:
                # Initialize point if None
                if user.point is None:
                    user.point = 0
                
                old_points = user.point
                user.point += points_to_add
                
                db.commit()
                
                print(f"✅ Points updated: {old_points} -> {user.point} (+{points_to_add})")
            
            # ✅ Build redirect URL with all parameters
            params = {
                "waste_type": waste_type,
                "point": point
            }
            
            if timestamp:
                params["timestamp"] = timestamp
            
            if dispose_id:
                params["id"] = dispose_id
            
            # ✅ Redirect to scan result page
            query_string = "&".join([f"{k}={v}" for k, v in params.items() if v])
            return RedirectResponse(
                url=f"/scan_result?{query_string}", 
                status_code=302
            )
            
        except Exception as e:
            print(f"❌ Error processing scan: {e}")
            db.rollback()
            return {"status": "error", "message": "Failed to process scan result"}
        finally:
            db.close()