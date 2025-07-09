from fasthtml.common import *
from function.component import ScrollTop

def profile_section(user):
    return Div(
        ScrollTop(),
        profile_content(user),
        _class="profile-wrapper"
    )

def profile_content(user):
    # ✅ Ensure point is displayed correctly, handle None values
    user_points = user.point if user.point is not None else 0
    
    return Div(
        Div(
            Img(src="/static/profile/default.png", _class="profile-img"),
            H2(user.username, _class="profile-name"),
            P(user.email, _class="profile-email"),
            Div(
                I("emoji_events", cls="material-symbols-rounded"),
                Span(f"{user_points} points"),
                _class="profile-badge"
            ),
            Div(
                Button("Edit Profile", _class="btn-edit"),
                Button("Logout", 
                       _class="btn-logout",
                       hx_post="/logout",
                       hx_target="#mainContent"),
                _class="profile-actions"
            ),
            _class="profile-card"
        ),
        _class="profile-container"
    )

def profile_empty():
    return Div(
        Div(
            Img(src="/static/logo/logo-dark.png", _class="empty-img"),
            H2("No profile data available", _class="empty-title"),
            P("You are not logged in. Please login to view your profile.", _class="empty-desc"),
            A("Login", href="/login", _class="btn-login"),
            _class="empty-card"
        ),
        _class="profile-wrapper"
    )