from fasthtml.common import *

# ==============================================================================
# DATA NAVBAR TERPUSAT
# ==============================================================================
NAV_ITEMS = [
    {"text": "Home", "href": "/landing", "icon": "home"},
    {"text": "Knowledge", "href": "/know", "icon": "lightbulb"},
    {"text": "Scan", "href": "/scan", "icon": "qr_code_scanner"},
    {"text": "Reward", "href": "/reward", "icon": "redeem"},
    {"text": "Account", "href": "/profile", "icon": "person"},
]

# ==============================================================================
# NAVBAR DESKTOP
# ==============================================================================
def navbar(user=None):
    home_href = "/dashboard" if user and user.email == "sortify01@gmail.com" else "/landing"

    navbar_links = []
    for item in NAV_ITEMS:
        href = home_href if item["text"] == "Home" else item["href"]
        navbar_links.append(
            A(item["text"], href=href, hx_get=href, hx_target="#mainContent", 
              cls="nav-link nav-item-desktop mx-2 p-0", data_path=item["href"])
        )

    if user:
        right_section = Div(
            Span(f"Hi, {user.username}", cls="navbar-text me-3 fw-bold"),
            Button("Logout", hx_post="/logout", hx_trigger="click", cls="btn btn-outline-danger btn-sm"),
            cls="d-flex align-items-center"
        )
    else:
        right_section = Div(
            A("Login", href="/login", hx_get="/login", hx_target="#mainContent", cls="btn btn-outline-success me-2"),
            A("Register", href="/register", hx_get="/register", hx_target="#mainContent", cls="btn btn-success"),
            cls="d-flex align-items-center"
        )

    return Nav(
        Div(
            A(Img(src="/static/logo/logo-dark.png", alt="Logo", style="height: 35px;"), href=home_href, cls="navbar-brand"),
            Div(*navbar_links, cls="navbar-nav mx-auto"),
            right_section,
            cls="container-fluid"
        ),
        cls="navbar navbar-expand-lg sticky-top bg-body-tertiary shadow-sm d-none d-lg-block"
    )

# ==============================================================================
# NAVBAR MOBILE (STRUKTUR DIPERBAIKI TOTAL)
# ==============================================================================
def navbar_mobile(user=None):
    home_href = "/dashboard" if user and user.email == "sortify01@gmail.com" else "/landing"

    mobile_nav_items = []
    for item in NAV_ITEMS:
        href = home_href if item["text"] == "Home" else item["href"]
        
        if item["text"] == "Scan":
            # Tombol Scan dibuat terpisah untuk styling yang benar
            link = A(
                Span(item["icon"], cls="material-symbols-rounded"),
                href=href, hx_get=href, hx_target="#mainContent",
                cls="scan-button", data_path=item["href"]
            )
            mobile_nav_items.append(Div(link, cls="scan-wrapper"))
        else:
            # Item navbar biasa
            link = A(
                Span(item["icon"], cls="material-symbols-rounded"),
                Span(item["text"], cls="small"),
                href=href, hx_get=href, hx_target="#mainContent",
                cls="nav-item-mobile", data_path=item["href"]
            )
            mobile_nav_items.append(link)

    return Div(
        Div(*mobile_nav_items, cls="mobile-navbar-inner"),
        cls="mobile-navbar-container d-lg-none"
    )

def ScrollTop():
    return Button(
        I("keyboard_arrow_up", cls="material-symbols-rounded text-white"),
        cls="scrolltop-button rounded-circle border-0",
        style="position: fixed; bottom: 25px; right: 20px; display: none; z-index: 1000;",
        onclick="window.scrollTo({top: 0, behavior: 'smooth'})"
    )