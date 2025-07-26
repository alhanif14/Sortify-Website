from fasthtml.common import *
from function.component import ScrollTop
from database.models import User, Voucher
from datetime import date

def redeem_alert(message, alert_type="success"):
    return Div(
        message,
        cls=f"alert alert-{alert_type} mt-4",
        role="alert"
    )

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

def reward_card(voucher: Voucher, user_points: int):
    modal_id = f"modal-{voucher.id}"
    can_redeem = user_points >= voucher.point_cost

    redeem_button = Button(
        "Redeem Points",
        hx_post=f"/redeem/{voucher.id}",
        hx_target="#reward-section",
        hx_swap="outerHTML",
        hx_confirm=f"Are you sure you want to redeem '{voucher.title}' for {voucher.point_cost} points?",
        cls=f"btn {'btn-success' if can_redeem else 'btn-secondary'} w-100 fw-semibold mt-3",
        disabled=not can_redeem,
        title="Not enough points" if not can_redeem else "Redeem this voucher"
    )

    return Div(
        Div(
            H5(voucher.title, cls="card-title fw-bold"),
            P(voucher.description, cls="card-text text-muted small"),
            Div(
                Span(f"{voucher.point_cost:,} Poin", cls="fw-bold fs-5 text-success"),
                A("See Details", href="#", cls="btn-link text-decoration-none small", data_bs_toggle="modal", data_bs_target=f"#{modal_id}"),
                cls="d-flex justify-content-between align-items-center mt-3"
            ),
            Div(redeem_button, cls="mt-auto pt-3"),
            cls="card-body d-flex flex-column"
        ),
        cls="card h-100 shadow-sm reward-card"
    )

def reward_content(user: User, available_vouchers: list[Voucher], success_message: str | None = None):
    return Div(
        Div(
            H2("Sortify Reward Center", cls="text-center fw-bolder"),
            P("Exchange the points you have collected for various interesting prizes below.", cls="text-center text-muted fs-5"),
            redeem_alert(success_message, "success") if success_message else "",
            user_points_display(user),
            cls="py-5"
        ),
        Div(
            *[Div(reward_card(voucher, user.point), cls="col-lg-3 col-md-4 col-sm-6 mb-4") for voucher in available_vouchers] if available_vouchers else P("No rewards available at the moment. Check back later!", cls="text-center text-muted"),
            cls="row"
        ),
        *[terms_and_conditions_modal(voucher) for voucher in available_vouchers],
    )

def reward_section(user: User, available_vouchers: list[Voucher], success_message: str | None = None):
    return Div(
        reward_content(
            user=user, 
            available_vouchers=available_vouchers, 
            success_message=success_message
        ),
        ScrollTop(),
        cls="container py-4",
        id="reward-section"
    )