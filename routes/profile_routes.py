from fasthtml.common import *
from function.profile import profile_section, profile_empty
from database.database import get_db_session
from database.models import User

def profile_routes(rt):
    @rt("/profile")
    def profile(request):
        user_id = request.session.get("user_id")
        if not user_id:
            return RedirectResponse(url="/login", status_code=302)
        
        # ✅ Gunakan context manager yang konsisten
        db = get_db_session()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return RedirectResponse(url="/login", status_code=302)

            # ✅ Return FastHTML component directly, bukan template
            return profile_section(user)
        finally:
            db.close()