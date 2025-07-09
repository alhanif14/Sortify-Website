from fasthtml.common import *
from function.component import ScrollTop
from datetime import datetime
import json

def scan1_content():
    return Div(
        Div(
            Img(src="/static/scan/QR.png", cls="scan1-illustration"),
            cls="text-start"
        ),
        Div(
            H3("Scan QR Code", cls="scan1-title"),
            P("Use the scan feature to earn points from the trash you throw away.", cls="scan1-desc"),
            P("💡 Make sure you are logged in to save points to your account.", cls="scan1-warning"),
            # ✅ Fixed button - should link to login, not scan
            A("Login / Register", 
              href="/login",
              hx_get="/login",
              hx_target="#mainContent", 
              cls="btn btn-success px-4 py-2 mt-3"),
            cls="text-center px-3"
        ),
        cls="container-fluids d-flex flex-column align-items-center justify-content-center"
    )

def scan1_section():
    return Div(
        scan1_content(),
        ScrollTop(),
        cls="scan1-page my-5 px-5"
    )

def scan_content():
    return Div(
        Video(id="camera", autoplay=True, cls="camera-preview"),
        Img(src="/static/logo/logo-dark.png", alt="Sortify Logo", cls="scan-logo"),
        Div(cls="scan-overlay"),
        Script(src="/static/js/scan.js"),
        cls="scan-page position-relative"
    )

def scan_section():
    return Div(scan_content())

# ✅ Add logged in scan content with user info
def scan_logged_content(user):
    return Div(
        Div(
            P(f"Welcome, {user.username}!", cls="scan-welcome"),
            P(f"Current Points: {user.point}", cls="scan-points"),
            cls="scan-user-info"
        ),
        Video(id="camera", autoplay=True, cls="camera-preview"),
        Img(src="/static/logo/logo-dark.png", alt="Sortify Logo", cls="scan-logo"),
        Div(cls="scan-overlay"),
        Script(src="/static/js/scan.js"),
        cls="scan-page position-relative"
    )

def scan_logged_section(user):
    return Div(scan_logged_content(user))

def get_waste_image(waste_type):
    return f"/static/scan/{waste_type}.png"

def get_point_per_waste(waste_type):
    return {
        "plastic": 40,
        "paper": 40,
        "organic": 30,
        "other": 10,
    }.get(waste_type.lower(), 0)

def scan_result_content(waste_types=None, point=None, timestamp=None, dispose_id=None, user=None):
    waste_types = waste_types.split(",") if waste_types else []
    
    # ✅ Use timestamp from QR code, fallback to current time
    if timestamp:
        try:
            # Parse timestamp if it's a string (ISO format or epoch)
            if isinstance(timestamp, str):
                if timestamp.isdigit():
                    # Epoch timestamp
                    date_obj = datetime.fromtimestamp(int(timestamp))
                else:
                    # ISO format
                    date_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                date_obj = datetime.fromtimestamp(timestamp)
            
            formatted_date = date_obj.strftime("%d %b %Y")
        except (ValueError, TypeError):
            formatted_date = datetime.now().strftime("%d %b %Y")
    else:
        formatted_date = datetime.now().strftime("%d %b %Y")
    
    # ✅ Use dispose_id from QR code, fallback to generated ID
    order_id = f"#{dispose_id}"
    
    username = user.username if user else "User"

    return Div(
        Div(
            Img(src="/static/logo/logo-dark.png", cls="receipt-logo"),
            P(formatted_date, cls="receipt-date"),
            H2(f"Hello, {username}!", cls="receipt-hello"),
            P("You have disposed these wastes in Sortify. Thank you for caring for the environment!", cls="receipt-msg"),
            Hr(),
            *[
                Div(
                    P(f"#{i+1}", cls="waste-index"),
                    Div(
                        Img(src=get_waste_image(w), cls="waste-img"),
                        P(w.capitalize(), cls="waste-name"),
                        cls="waste-left"
                    ),
                    P(f"+{get_point_per_waste(w)} pts", cls="waste-point"),
                    Hr(),
                    cls="waste-row"
                ) for i, w in enumerate(waste_types)
            ],
            Div(
                P("Total", cls="receipt-total-label"),
                P(f"{point} pts", cls="receipt-total"),
                cls="receipt-total-row"
            ),
            P(f"Dispose id: {order_id}", cls="receipt-order"),
            A("Check your point!", href="/profile", hx_get="/profile", hx_target="#mainContent", cls="btn btn-primary mt-3"),
            cls="receipt-box"
        ),
        cls="receipt-page d-flex justify-content-center align-items-center"
    )

def scan_result_section(request, user=None):
    waste_type = request.query_params.get("waste_type", "")
    point = request.query_params.get("point", "0")
    timestamp = request.query_params.get("timestamp", None)
    dispose_id = request.query_params.get("id", None)
    
    return Div(scan_result_content(waste_type, point, timestamp, dispose_id, user))