from fasthtml.common import *
from function.landing import landing_section, dashboard_section
from database.database import get_current_user

def landing_routes(rt):
    @rt("/landing")
    def landing(request):
        user = get_current_user(request)
        return landing_section(user=user)

    @rt("/dashboard")
    def dashboard():
        return dashboard_section()
