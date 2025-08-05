from fasthtml.common import *
from function.component import ScrollTop
from database.models import User, Voucher
from datetime import date

def redeem_alert(message, alert_type="success"):
    return Div(message, cls=f"alert alert-{alert_type} mt-4", role="alert")

def user_points_display(user: User):
    return Div(
        Span("Your Current Points:", cls="me-2"),
        Span(f"{user.point:,}", cls="badge bg-success fs-5 rounded-pill"),
        id="user-points",
        cls="d-flex justify-content-center align-items-center mt-4",
    )

def terms_and_conditions_modal(voucher: Voucher):
    modal_id = f"modal-{voucher.id}"
    terms_list = voucher.terms_conditions.split('\n') if voucher.terms_conditions else []
    return Div(
        Div(
            Div(
                Div(
                    H5("Term & Condition", cls="modal-title fw-bold", id=f"{modal_id}-label"),
                    Button(type="button", cls="btn-close", data_bs_dismiss="modal", aria_label="Close")
                , cls="modal-header"),
                Div(
                    P(Strong(voucher.title), cls="mb-3"),
                    Ul(*[Li(term, cls="mb-2") for term in terms_list])
                , cls="modal-body"),
                Div(
                    Button("Close", type="button", cls="btn btn-secondary", data_bs_dismiss="modal")
                , cls="modal-footer")
            , cls="modal-content")
        , cls="modal-dialog modal-dialog-centered")
    , id=modal_id, cls="modal fade", tabindex="-1", aria_labelledby=f"{modal_id}-label", aria_hidden="true")

def admin_reward_form(voucher: Voucher | None = None):
    is_edit_mode = voucher is not None
    def value(attr_name):
        val = getattr(voucher, attr_name, '')
        return str(val) if val is not None else ''

    return Form(
        Input(type="hidden", name="voucher_id", value=value('id')),
        
        Div(Label("Voucher Title", html_for="title", cls="form-label"),
            Input(type="text", name="title", id="title", value=value('title'), required=True, cls="form-control"),
            cls="mb-3"),

        Div(Label("Description", html_for="description", cls="form-label"),
            Textarea(value('description'), name="description", id="description", required=True, cls="form-control", rows="3"),
            cls="mb-3"),

        Div(Label("Point Cost", html_for="point_cost", cls="form-label"),
            Input(type="number", name="point_cost", id="point_cost", value=value('point_cost'), required=True, cls="form-control"),
            cls="mb-3"),

        Div(
            Div(Label("Start Date", html_for="start_date", cls="form-label"),
                Input(type="date", name="start_date", id="start_date", value=value('start_date'), required=True, cls="form-control"),
                cls="col"),
            Div(Label("End Date", html_for="end_date", cls="form-label"),
                Input(type="date", name="end_date", id="end_date", value=value('end_date'), required=True, cls="form-control"),
                cls="col"),
            cls="row mb-3"),

        Div(Label("Terms & Conditions (one per line)", html_for="terms_conditions", cls="form-label"),
            Textarea(value('terms_conditions'), name="terms_conditions", id="terms_conditions", cls="form-control", rows="4"),
            cls="mb-3"),
        
        Button("Save Reward", type="submit", cls="btn btn-success w-100", data_bs_dismiss="modal"),

        hx_post="/admin/voucher/save",
        hx_target="#reward-section",
        hx_swap="outerHTML"
    )

def reward_card(voucher: Voucher, user_points: int, status: str, user: User | None = None):
    start_date_str = voucher.start_date.strftime('%d %b %Y')
    end_date_str = voucher.end_date.strftime('%d %b %Y')
    
    card_footer = None
    if status == 'available':
        can_redeem = user_points >= voucher.point_cost
        card_footer = Div(
            Button("Redeem Points", hx_post=f"/redeem/{voucher.id}", hx_target="#reward-section", hx_swap="outerHTML",
                   hx_confirm=f"Redeem '{voucher.title}'?",
                   cls=f"btn {'btn-success' if can_redeem else 'btn-secondary'} w-100 fw-semibold mt-3",
                   disabled=not can_redeem, title="Not enough points" if not can_redeem else "Redeem this voucher"),
            cls="mt-auto pt-3"
        )
    else:
        badge_color = "bg-info-subtle text-info-emphasis" if status == 'coming_soon' else "bg-secondary-subtle"
        card_footer = Div(
            Span(voucher.status_text, cls=f"badge rounded-pill w-100 {badge_color} py-2 fs-6 fw-normal"),
            cls="mt-auto pt-3"
        )
    
    def is_admin(u):
        return u and u.email == "sortify01@gmail.com"
        
    return Div(
        Div(
            Div(
                H5(voucher.title, cls="card-title fw-bold"),
                A(I("edit", cls="material-symbols-rounded"),
                  data_bs_toggle="modal", data_bs_target="#adminRewardModal",
                  hx_get=f"/admin/voucher/form/{voucher.id}",
                  hx_target="#adminModalContent",
                  cls="btn btn-sm btn-outline-secondary ms-auto"
                ) if is_admin(user) else ""
            , cls="d-flex align-items-center"),
            
            P(voucher.description, cls="card-text text-muted small"),
            P(I("calendar_month", cls="material-symbols-rounded me-1", style="font-size: 1em; vertical-align: text-bottom;"),
              f" {start_date_str} - {end_date_str}", cls="card-text text-muted small mt-2"),
            Div(
                Span(f"{voucher.point_cost:,} Poin", cls="fw-bold fs-5 text-success"),
                A("See Details", href="#", cls="btn-link text-decoration-none small", data_bs_toggle="modal", data_bs_target=f"#modal-{voucher.id}"),
                cls="d-flex justify-content-between align-items-center mt-3"
            ),
            card_footer,
            cls="card-body d-flex flex-column"
        ),
        cls="card h-100 shadow-sm reward-card"
    )

def reward_content(user, available_vouchers, coming_soon_vouchers, past_vouchers, success_message=None):
    all_vouchers = available_vouchers + coming_soon_vouchers + past_vouchers
    def is_admin(u):
        return u and u.email == "sortify01@gmail.com"

    point_info_data = [
        {"category": "Recycle (Plastic, Glass, Metal)", "points": 40, "color": "primary"},
        {"category": "Paper (Newspapers, Cardboard)", "points": 40, "color": "warning"},
        {"category": "Organic (Food scraps, Leaves)", "points": 30, "color": "success"},
        {"category": "Other (Residual/Non-recyclable)", "points": 10, "color": "secondary"},
    ]
    def point_info_item(item):
        return Div(
            Span(item["category"], cls="fw-medium"),
            Span(f"{item['points']} points", cls=f"badge rounded-pill bg-{item['color']}-subtle text-{item['color']}-emphasis"),
            cls="d-flex justify-content-between align-items-center list-group-item"
        )

    return Div(
        Div(
            Div(
                I("redeem", cls="material-symbols-rounded text-success mb-3", style="font-size: 4rem;"),
                H1("Sortify Reward Center", cls="fw-bolder"),
                P("Redeem your points for exclusive vouchers, merchandise, or donations!", cls="fs-5 text-muted"),
                Div(
                     Span("Your Current Points:", cls="fs-4"),
                     Span(f"{user.point:,}", cls="badge bg-success fs-5 rounded-pill ms-3"),
                     cls="d-flex align-items-center mt-4"
                ),
                cls="col-lg-7 mb-4 mb-lg-0"
            ),
            Div(
                Div(
                 H5("How to Earn Points?", cls="fw-bold mb-3"),
                 Div(*[point_info_item(item) for item in point_info_data], cls="list-group list-group-flush"),
                 cls="card-body"
                 ),
                  cls="card shadow-sm h-100 col-lg-5"),
            cls="row align-items-center mb-5 p-4"
    ),

        Div(
            P("Need help or have question about reward?", cls="mb-1 text-muted"),
            A(
                "Contact Us For Details",
                href="mailto:sortify01@gmail.com?subject=Question about Sortify Reward",
                cls="fw-bold text-success"
            ),
            cls="text-center p-3 my-4 bg-success-subtle rounded-3 border"
        ),
        redeem_alert(success_message, "success") if success_message else "",

        Div(
            H3("Available Rewards"),
            Button(
                I("add", cls="material-symbols-rounded"),
                cls="btn btn-success ms-auto", data_bs_toggle="modal", data_bs_target="#adminRewardModal",
                hx_get="/admin/voucher/form", hx_target="#adminModalContent"
            ) if is_admin(user) else ""
        , cls="d-flex align-items-center mt-5 mb-3 border-top pt-4"),
        
        Div(
            *[Div(reward_card(v, user.point, 'available', user), cls="col-lg-3 col-md-4 col-sm-6 mb-4") for v in available_vouchers]
            if available_vouchers else P("No rewards available at the moment.", cls="text-muted"),
            cls="row mb-5 ps-3"
        ),
        
        *[Div(
            H3("Coming Soon", cls="mb-3 mt-5 border-top pt-4"),
            Div(*[Div(reward_card(v, user.point, 'coming_soon', user), cls="col-lg-3 col-md-4 col-sm-6 mb-4") for v in coming_soon_vouchers], cls="row mb-5")
        )] if coming_soon_vouchers else "",
        
        *[Div(
            H3("Redeemed & Expired", cls="mb-3 mt-5 border-top pt-4"),
            Div(*[Div(reward_card(v, user.point, 'past', user), cls="col-lg-3 col-md-4 col-sm-6 mb-4") for v in past_vouchers], cls="row mb-5")
        )] if past_vouchers else "",

        *[terms_and_conditions_modal(v) for v in all_vouchers],
    )

def reward_section(user, available_vouchers, coming_soon_vouchers, past_vouchers, success_message=None):
    return Div(
        Div(
            Div(
                Div(
                    Div(
                        H5("Manage Reward", cls="modal-title"),
                        Button(type="button", cls="btn-close", data_bs_dismiss="modal", aria_label="Close")
                    , cls="modal-header"),
                    Div(cls="modal-body", id="adminModalContent")
                , cls="modal-content")
            , cls="modal-dialog modal-dialog-scrollable")
        , cls="modal fade", id="adminRewardModal", tabindex="-1"),
        reward_content(
            user, available_vouchers, coming_soon_vouchers, past_vouchers, success_message
        ),
        ScrollTop(),
        cls="container py-4",
        id="reward-section"
    )

def reward_unauthenticated_content():
    return Div(
        Div(
            I("redeem", cls="material-symbols-rounded", style="font-size: 100px; color: #198754;"),
            cls="text-center my-4"
        ),
        Div(
            H3("Rewards Await!", cls="scan1-title"),
            P("See the exciting rewards you can get by sorting waste.", cls="scan1-desc"),
            P("💡 Log in first to see available rewards and track your points.", cls="scan1-warning"),
            A("Login / Register", 
              href="/login",
              hx_get="/login",
              hx_target="#mainContent", 
              cls="btn btn-success px-4 py-2 mt-3 mb-5"),
            cls="text-center px-3"
        ),
        cls="container-fluids d-flex flex-column align-items-center justify-content-center"
    )

def reward_unauthenticated_section():
    return Div(
        reward_unauthenticated_content(),
        ScrollTop(),
        cls="scan1-page my-5 px-5"
    )