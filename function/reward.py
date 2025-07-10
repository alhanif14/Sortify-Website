from fasthtml.common import *
from function.component import ScrollTop

rewards_data = [
    {
        "id": "voucher_50k",
        "title": "Shopping Voucher IDR 50.000",
        "points": 2500,
        "description": "Redeem your points for a shopping voucher at nearby convenience stores.",
        "terms": [
           "Voucher is only valid at Indomaret & Alfamart.",
            "Cannot be combined with other promotions.",
            "Voucher is valid for 30 days after redemption.",
            "Only valid for a single transaction."
        ]
    },
    {
        "id": "gopay_balance",
        "title": "GoPay Balance IDR 25.000",
        "points": 1500,
        "description": "Get free GoPay balance to shop or pay bills.",
        "terms": [
            "Make sure the phone number registered on Sortify matches your GoPay account.",
            "Balance will be sent within a maximum of 2x24 hours after redemption.",
            "Sortify is not responsible for any incorrect phone number input."
        ]
    },
    {
        "id": "donation_tree",
        "title": "Donation of 1 Tree",
        "points": 1000,
        "description": "Convert your points to plant one tree in your name.",
        "terms": [
            "The tree will be planted in collaboration with LindungiHutan.",
            "You will receive a digital certificate in your name.",
            "The planting location will be determined by our partner."
        ]
    },
    {
        "id": "merchandise_totebag",
        "title": "Exclusive Sortify Totebag",
        "points": 3000,
        "description": "Take home a cool eco-friendly tote bag from Sortify.",
        "terms": [
            "Limited stock, first come first served.",
            "Shipping costs are borne by the user.",
            "Estimated delivery 5-7 working days."
        ]
    }
]

def terms_and_conditions_modal(reward):
    modal_id = f"modal-{reward['id']}"
    return Div(
        Div(
            Div(
                # Header Modal
                Div(
                    H5(f"Syarat & Ketentuan", cls="modal-title fw-bold", id=f"{modal_id}-label"),
                    Button(type="button", cls="btn-close", data_bs_dismiss="modal", aria_label="Close")
                , cls="modal-header"),
                # Body Modal
                Div(
                    P(Strong(reward['title']), cls="mb-3"),
                    Ul(*[Li(term, cls="mb-2") for term in reward['terms']], cls="list-unstyled modal-terms-list")
                , cls="modal-body"),
                # Footer Modal
                Div(
                    Button("Close", type="button", cls="btn btn-secondary", data_bs_dismiss="modal")
                , cls="modal-footer")
            , cls="modal-content")
        , cls="modal-dialog modal-dialog-centered")
    , id=modal_id, cls="modal fade", tabindex="-1", aria_labelledby=f"{modal_id}-label", aria_hidden="true")

def reward_card(reward):
    modal_id = f"modal-{reward['id']}"
    return Div(
        Div(
            H5(reward["title"], cls="card-title fw-bold"),
            P(reward["description"], cls="card-text text-muted small"),
            Div(
                Span(f"{reward['points']:,} Poin", cls="fw-bold fs-5 text-success"),
                A("See Details", href="#", cls="btn-link text-decoration-none small", data_bs_toggle="modal", data_bs_target=f"#{modal_id}"),
                cls="d-flex justify-content-between align-items-center mt-3"
            ),
            Div(
                A("Redeem Points", href="#", cls="btn btn-success w-100 fw-semibold mt-3"),
                cls="mt-auto pt-3"
            ),
            cls="card-body d-flex flex-column"
        ),
        cls="card h-100 shadow-sm reward-card"
    )

def reward_content():
    user_points = 5210
    
    return Div(
        Div(
            H2("Sortify Reward Center", cls="text-center fw-bolder"),
            P("Exchange the points you have collected for various interesting prizes below.", cls="text-center text-muted fs-5"),
            Div(
                Span("Your Current Points:", cls="me-2"),
                Span(f"{user_points:,}", cls="badge bg-success fs-5 rounded-pill"),
                cls="d-flex justify-content-center align-items-center mt-4"
            ),
            cls="py-5"
        ),
        Div(
            *[Div(reward_card(reward), cls="col-lg-3 col-md-4 col-sm-6 mb-4") for reward in rewards_data],
            cls="row"
        ),
        *[terms_and_conditions_modal(reward) for reward in rewards_data]
    )

def reward_section():
    return Div(
        reward_content(),
        ScrollTop(),
        cls="container py-4"
    )
