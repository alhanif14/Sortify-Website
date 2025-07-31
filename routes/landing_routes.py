from fasthtml.common import *
from function.landing import full_leaderboard_modal_content, disposal_logs_card_content, landing_section, dashboard_section
from database.database import get_current_user, get_db_session
from database.models import User, WasteDetectionLog
from starlette.requests import Request
from starlette.responses import HTMLResponse
from sqlalchemy import desc, asc, or_
import math

def is_admin(u):
    return u and u.email == "sortify01@gmail.com"

def landing_routes(rt):
    @rt("/dashboard/leaderboard-all")
    def get_full_leaderboard(request: Request):
        user = get_current_user(request)
        if not is_admin(user): return HTMLResponse("Forbidden", status_code=403)
        
        db = get_db_session()
        try:
            all_users = db.query(User).order_by(desc(User.point)).all()
            return full_leaderboard_modal_content(all_users)
        finally:
            db.close()

    @rt("/dashboard/logs-table")
    def get_logs_table(request: Request):
        user = get_current_user(request)
        if not is_admin(user): return HTMLResponse("Forbidden", status_code=403)
        
        db = get_db_session()
        try:
            page = int(request.query_params.get("page", 1))
            search = request.query_params.get("search", "")
            sort_by = request.query_params.get("sort_by", "timestamp")
            order = request.query_params.get("order", "desc")
            
            ITEMS_PER_PAGE = 5
            
            query = db.query(WasteDetectionLog)
            
            if search:
                search_term = f"%{search}%"
                search_filters = [
                    WasteDetectionLog.username.ilike(search_term),
                    WasteDetectionLog.waste_type.ilike(search_term)
                ]
                if search.isdigit():
                    search_filters.append(WasteDetectionLog.id == int(search))
                
                query = query.filter(or_(*search_filters))
            sort_column = getattr(WasteDetectionLog, sort_by, WasteDetectionLog.timestamp)
            order_func = desc if order == "desc" else asc
            query = query.order_by(order_func(sort_column))
            
            total_items = query.count()
            total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
            
            logs = query.offset((page - 1) * ITEMS_PER_PAGE).limit(ITEMS_PER_PAGE).all()
            
            return disposal_logs_card_content(
                logs=logs, page=page, total_pages=total_pages, 
                search=search, sort_by=sort_by, order=order
            )
        finally:
            db.close()

    @rt("/landing")
    def landing(request):
        user = get_current_user(request)
        return landing_section(user=user)

    @rt("/dashboard")
    def dashboard():
        return dashboard_section()
