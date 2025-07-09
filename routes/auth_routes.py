from function.auth import login_section, register_section
from starlette.responses import RedirectResponse
from database.database import get_db_session
from database.models import User
from fasthtml.common import *

def auth_routes(rt):
    @rt("/login")
    def login(request):
        error = request.query_params.get("error", "")
        error_message = ""
        
        if error == "missing":
            error_message = "Email and password are required"
        elif error == "invalid":
            error_message = "Invalid email or password"
        elif error == "required":
            error_message = "Please login to access this page"
        return login_section(error_message) 
    @rt("/register")
    def register(request):
        error = request.query_params.get("error", "")
        success = request.query_params.get("success", "")
        error_message = ""
        success_message = ""
        
        if error == "confirm":
            error_message = "Passwords do not match"
        elif error == "email_exists":
            error_message = "Email already exists"
        elif error == "missing":
            error_message = "All fields are required"
        elif error == "db_error":
            error_message = "Registration failed. Please try again"
        elif success == "1":
            success_message = "Registration successful! Please login with your credentials"
            
        return register_section(error_message, success_message)

    @rt("/login_session", methods=["POST"])
    def login_post(request, email: str = "", password: str = ""):
        if not email or not password:
            if request.headers.get("HX-Request"):
                return Div(
                    Div("Email and password are required", cls="alert alert-danger"),
                    Script("document.getElementById('auth-messages').scrollIntoView({behavior: 'smooth', block: 'center'});"),
                    cls="messages-container",
                    id="auth-messages"
                )
            return RedirectResponse(url="/login?error=missing", status_code=302)
        
        db = get_db_session()
        try:
            user = db.query(User).filter(User.email == email, User.password == password).first()
            if user:
                request.session["user_id"] = user.id
                
                if request.headers.get("HX-Request"):
                    from fasthtml.common import Response
                    response = Response()
                    response.headers["HX-Refresh"] = "true"  # Forces full page refresh
                    return response
                else:
                    return RedirectResponse(url="/", status_code=302)
            else:
                if request.headers.get("HX-Request"):
                    return Div(
                        Div("Invalid email or password", cls="alert alert-danger"),
                        Script("document.getElementById('auth-messages').scrollIntoView({behavior: 'smooth', block: 'center'});"),
                        cls="messages-container",
                        id="auth-messages"
                    )
                return RedirectResponse(url="/login?error=invalid", status_code=302)
        except Exception as e:
            print(f"Login error: {e}")
            if request.headers.get("HX-Request"):
                return Div(
                    Div("Invalid email or password", cls="alert alert-danger"),
                    Script("document.getElementById('auth-messages').scrollIntoView({behavior: 'smooth', block: 'center'});"),
                    cls="messages-container",
                    id="auth-messages"
                )
            return RedirectResponse(url="/login?error=invalid", status_code=302)
        finally:
            db.close()

    @rt("/register_session", methods=["POST"])
    def register_post(request, username: str = "", email: str = "", password: str = "", confirm_password: str = ""):
        if not username or not email or not password or not confirm_password:
            if request.headers.get("HX-Request"):
                return Div(
                    Div("All fields are required", cls="alert alert-danger"),
                    Script("document.getElementById('auth-messages').scrollIntoView({behavior: 'smooth', block: 'center'});"),
                    cls="messages-container",
                    id="auth-messages"
                )
            return RedirectResponse(url="/register?error=missing", status_code=302)
            
        if password != confirm_password:
            if request.headers.get("HX-Request"):
                return Div(
                    Div("Passwords do not match", cls="alert alert-danger"),
                    Script("document.getElementById('auth-messages').scrollIntoView({behavior: 'smooth', block: 'center'});"),
                    cls="messages-container",
                    id="auth-messages"
                )
            return RedirectResponse(url="/register?error=confirm", status_code=302)
        
        db = get_db_session()
        try:
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                if request.headers.get("HX-Request"):
                    return Div(
                        Div("Email already exists", cls="alert alert-danger"),
                        Script("document.getElementById('auth-messages').scrollIntoView({behavior: 'smooth', block: 'center'});"),
                        cls="messages-container",
                        id="auth-messages"
                    )
                return RedirectResponse(url="/register?error=email_exists", status_code=302)
            
            new_user = User(username=username, email=email, password=password)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            if request.headers.get("HX-Request"):
                return Div(
                    Div(
                        "Registration successful! ",
                        A("Click here to login", href="/login", hx_get="/login", hx_target="#mainContent", cls="link"),
                        cls="alert alert-success"
                    ),
                    Script("document.getElementById('auth-messages').scrollIntoView({behavior: 'smooth', block: 'center'});"),
                    cls="messages-container",
                    id="auth-messages"
                )
            
            return RedirectResponse(url="/register?success=1", status_code=302)
            
        except Exception as e:
            print(f"Registration error: {e}")
            db.rollback()
            if request.headers.get("HX-Request"):
                return Div(
                    Div("Registration failed. Please try again", cls="alert alert-danger"),
                    Script("document.getElementById('auth-messages').scrollIntoView({behavior: 'smooth', block: 'center'});"),
                    cls="messages-container",
                    id="auth-messages"
                )
            return RedirectResponse(url="/register?error=db_error", status_code=302)
        finally:
            db.close()

    @rt("/logout")
    def logout(request):
        request.session.clear()
        
        if request.headers.get("HX-Request"):
            return Script("window.location.reload();")
        else:
            return RedirectResponse(url="/", status_code=302)