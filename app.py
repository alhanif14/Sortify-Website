from fasthtml.common import *
import os
from function.landing import landing_section, dashboard_section
from function.component import navbar, navbar_mobile
from routes.scan_routes import scan_routes
from routes.landing_routes import landing_routes
from routes.reward_routes import reward_routes
from routes.know_routes import know_routes
from routes.profile_routes import profile_routes
from routes.auth_routes import auth_routes
from starlette.middleware.sessions import SessionMiddleware
from database.database import get_current_user, Base, engine
from database.models import models
from starlette.responses import RedirectResponse
import uvicorn
from dotenv import load_dotenv
load_dotenv()

app, rt = fast_app(live=True, pico=False)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

landing_routes(rt)
scan_routes(rt)
reward_routes(rt)
know_routes(rt)
profile_routes(rt)
auth_routes(rt)

def main_content(user=None):
    if user and user.email == "sortify01@gmail.com":
        content = dashboard_section()
    else:
        content = landing_section(user)

    return Div(
        content,
        cls="main h-100 w-100 mb-3",
        id="mainContent"
    )

@rt("/")
def landing(request):
    user = get_current_user(request)
    return Html(
        Head(
            Meta(name="viewport", content="width=device-width"),
            Title("Sortify"),
            Link(href="/static/css/style.css", rel="stylesheet"),
            Link(href="/static/css/navbar.css", rel="stylesheet"),
            Link(href="/static/css/landing.css", rel="stylesheet"),
            Link(href="/static/css/scan.css", rel="stylesheet"),
            Link(href="/static/css/reward.css", rel="stylesheet"),
            Link(href="/static/css/know.css", rel="stylesheet"),
            Link(href="/static/css/profile.css", rel="stylesheet"),
            Link(href="/static/css/auth.css", rel="stylesheet"),
            Link(href="/static/css/detail_reward.css", rel="stylesheet"),
            Link(href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@300;600&display=swap", rel="stylesheet"),
            Link(href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css", rel="stylesheet"),
            Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"),
            Link(href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded", rel="stylesheet"),
            Script(type="module", src="/static/js/countUp.min.js"),
            Script(type="module", src="/static/js/initCountUp.js"),
            Script(type="module", src="/static/js/script.js"),
            Script(src="https://unpkg.com/jsqr/dist/jsQR.js", defer=True),
            Script(type="module", src="/static/js/scan.js"),
            Script(src="https://unpkg.com/htmx.org@1.9.12", defer=True),
            Script(src="https://cdn.jsdelivr.net/npm/chart.js")
        ),
        Body(
        navbar(user),
        navbar_mobile(user),
        main_content(user),
        ),
    )

Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0")
    