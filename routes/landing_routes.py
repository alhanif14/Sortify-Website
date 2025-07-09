from fasthtml.common import *
from function.landing import landing_section, dashboard_section

def landing_routes(rt):
    @rt("/landing")
    def landing():
        return landing_section()
    
    @rt("/dashboard")
    def dashboard():
        return dashboard_section()
