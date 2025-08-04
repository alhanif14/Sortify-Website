from fasthtml.common import *
from function.profile import profile_section, user_disposal_logs_content
from database.database import get_db_session, get_current_user
from database.models import User, WasteDetectionLog
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from sqlalchemy import desc, asc, or_, func
import math

def profile_routes(rt):
    @rt("/profile")
    def profile(request: Request):
        user = get_current_user(request)
        if not user:
            return RedirectResponse(url="/login", status_code=302)
        
        db = get_db_session()
        try:
            stats = db.query(
                WasteDetectionLog.waste_type, 
                func.count(WasteDetectionLog.id)
            ).filter(
                WasteDetectionLog.username == user.username
            ).group_by(
                WasteDetectionLog.waste_type
            ).all()

            category_map = {
                "Plastic": "Recycle",
                "Recycle": "Recycle",
                "Paper": "Paper",
                "Organic": "Organic"
            }

            disposal_stats = {"Recycle": 0, "Paper": 0, "Organic": 0, "Other": 0}
            
            for waste_type_string, count in stats:
                individual_types = [s.strip() for s in waste_type_string.split(',')]
                
                for individual_type in individual_types:
                    main_category = category_map.get(individual_type.capitalize(), "Other")
                    
                    if main_category in disposal_stats:
                        disposal_stats[main_category] += count
            return profile_section(user, disposal_stats)
        finally:
            db.close()

    @rt("/profile/logs")
    def get_user_logs_table(request: Request):
        user = get_current_user(request)
        if not user:
            return HTMLResponse("Unauthorized", status_code=401)
        
        db = get_db_session()
        try:
            page = int(request.query_params.get("page", 1))
            search = request.query_params.get("search", "")
            sort_by = request.query_params.get("sort_by", "timestamp")
            order = request.query_params.get("order", "desc")
            
            ITEMS_PER_PAGE = 8
            
            query = db.query(WasteDetectionLog).filter(WasteDetectionLog.username == user.username)
            
            if search:
                search_term = f"%{search}%"
                query = query.filter(WasteDetectionLog.waste_type.ilike(search_term))

            sort_column = getattr(WasteDetectionLog, sort_by, WasteDetectionLog.timestamp)
            order_func = desc if order == "desc" else asc
            query = query.order_by(order_func(sort_column))
            
            total_items = query.count()
            total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
            
            logs = query.offset((page - 1) * ITEMS_PER_PAGE).limit(ITEMS_PER_PAGE).all()
            
            return user_disposal_logs_content(
                logs=logs, page=page, total_pages=total_pages, 
                search=search, sort_by=sort_by, order=order
            )
        finally:
            db.close()