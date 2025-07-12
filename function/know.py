from fasthtml.common import *
from function.component import ScrollTop

knowledge_data = [
    {
        "title": "Plastic Waste",
        "image_src": "/static/knowledge/plastic.png",
        "description": "Plastic waste is all used items made from plastic, such as bottles, packaging, and plastic bags. This material is very difficult to decompose and can last hundreds of years in the environment.",
        "examples": "Water bottles, food wrappers, straws, plastic bags.",
        "fun_fact": "Every minute, one million plastic bottles are bought around the world!",
        "theme_color": "primary"
    },
    {
        "title": "Paper Waste",
        "image_src": "/static/knowledge/paper.jpg",
        "description": "Paper waste includes used paper products, such as newspapers, magazines, and cardboard. Unlike plastic, paper can decompose and be recycled easily if managed properly.",
        "examples": "Newspapers, HVS paper, cardboard, magazines, envelopes.",
        "fun_fact": "Recycling one ton of paper can save 17 trees and 26,500 liters of water!",
        "theme_color": "warning"
    },
    {
        "title": "Organic Waste",
        "image_src": "/static/knowledge/organic.jpg",
        "description": "Organic waste is all material that can decompose naturally, originating from plants or animals. This waste can be processed into compost to enrich the soil.",
        "examples": "Fruit and vegetable scraps, dry leaves, coffee grounds, eggshells.",
        "fun_fact": "In some countries, organic waste accounts for more than 50% of total household waste!",
        "theme_color": "success"
    },
    {
        "title": "Other Waste",
        "image_src": "/static/knowledge/others.jpg",
        "description": "This category includes all types of waste that are not plastic, paper, or organic. It can be hazardous waste, electronic waste (e-waste), glass, and mixed materials.",
        "examples": "Batteries, light bulbs, electronic devices, ceramics, glass.",
        "fun_fact": "Electronic waste (e-waste) is the fastest-growing waste stream in the world!",
        "theme_color": "secondary"
    }
]

def knowledge_card(data):
    return Div(
        Img(src=data["image_src"], cls="card-img-top knowledge-card-img", alt=data["title"]),
        Div(
            H5(data["title"], cls=f"card-title fw-bold text-{data['theme_color']}"),
            P(data["description"], cls="card-text mb-3"),
            P(Strong("Examples: "), data["examples"], cls="card-text small text-muted"),
            Div(
                P(Strong("🧠 Fun Fact:"), cls="mb-1"),
                P(data["fun_fact"], cls="mb-0 fst-italic"),
                cls=f"fun-fact-box mt-auto bg-{data['theme_color']}-subtle"
            ),
            cls="card-body d-flex flex-column"
        ),
        cls=f"card h-100 shadow-sm border-{data['theme_color']}"
    )

def know_content():
    return Div(
        Div(
            H2("Waste Knowledge Centre", cls="text-center fw-bolder"),
            P("Understand the different types of waste to help make the recycling process more effective.", cls="text-center text-muted fs-5 mb-5"),
            cls="mb-5"
        ),
        Div(
            *[Div(knowledge_card(item), cls="col-lg-3 col-md-6 mb-4") for item in knowledge_data],
            cls="row"
        ),
    )

def know_section():
    return Div(
        know_content(),
        ScrollTop(),
        cls="knowledge-page container-fluid px-4 px-lg-5 py-5"
    )
