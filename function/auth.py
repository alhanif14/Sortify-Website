from fasthtml.common import *

def form_field(icon_name, placeholder, input_type="text", name=""):
    return Div(
        I(icon_name, cls="material-symbols-rounded"),
        Input(type=input_type, placeholder=placeholder, name=name, cls="form-input"),
        cls="input-group"
    )

def form_password_field(icon_name, placeholder, name=""):
    return Div(
        I(icon_name, cls="material-symbols-rounded"),
        Div(
            Input(type="password", placeholder=placeholder, name=name, cls="form-input password-input", id=name),
            I("visibility", cls="material-symbols-rounded toggle-password", **{"data-target": name}),
            cls="password-wrapper"
        ),
        cls="input-group"
    )


def register_content(error_message="", success_message=""):
    return Div(
        Div(
            Div(
                error_message,
                cls="alert alert-danger"
            ) if error_message else "",
            
            # Success message
            Div(
                success_message,
                cls="alert alert-success"
            ) if success_message else "",
            
            cls="messages-container",
            id="auth-messages"
        ),
        
        Form(
            Img(src="/static/logo/logo-dark.png", cls="logo"),
            H2("Your journey starts here", cls="title"),
            P("Take the first step", cls="subtitle"),

            form_field("mail", "E-mail", "email", "email"),
            form_field("person", "Username", "text", "username"),
            form_password_field("lock", "Password", "password"),
            form_password_field("lock", "Confirm password", "confirm_password"),

            Button("Sign up", cls="btn-submit"),

            Div(Hr(), Span("or"), Hr(), cls="separator"),
            Div(I("google", cls="material-symbols-rounded icon-social"), cls="social-icons"),

            P(
                "Already have an account? ",
                A("Sign in", href="/login", hx_get="/login", hx_target="#mainContent", cls="link"),
                cls="auth-toggle"
            ),

            method="post",
            action="/register_session", 
            hx_post="/register_session",
            hx_target="#auth-messages",
            cls="auth-container"
        ),
        cls="register-page"
    )


def register_section(error_message="", success_message=""):
    return register_content(error_message, success_message)


def login_content(error_message=""):
    return Div(
        Div(
            # Error message
            Div(
                error_message,
                cls="alert alert-danger"
            ) if error_message else "",
            
            cls="messages-container",
            id="auth-messages" 
        ),
        
        Form(
            Img(src="/static/logo/logo-dark.png", cls="logo"),
            H2("Welcome back", cls="title"),
            P("Let's continue sorting!", cls="subtitle"),

            form_field("mail", "E-mail", "email", "email"),
            form_password_field("lock", "Password", "password"),

            Button("Login", cls="btn-submit"),

            Div(Hr(), Span("or"), Hr(), cls="separator"),
            Div(I("google", cls="material-symbols-rounded icon-social"), cls="social-icons"),

            P(
                "Don't have an account? ",
                A("Sign up", href="/register", hx_get="/register", hx_target="#mainContent", cls="link"),
                cls="auth-toggle"
            ),

            method="post",
            action="/login_session",
            hx_post="/login_session",
            hx_target="#auth-messages",
            cls="auth-container"
        ),
        cls="login-page"
    )


def login_section(error_message=""):
    return login_content(error_message)