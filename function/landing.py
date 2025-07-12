from fasthtml.common import *
from function.component import ScrollTop
from database.database import get_db_session
from database.models import User, WasteDetectionLog
from sqlalchemy import desc
from datetime import datetime, timedelta
import json

def landing_hero():
    return Div(
        Div(
            Div(
                H1("The Future Is Cleaner,", cls="display-4 fw-bolder text-center text-lg-start"),
                H1(Span("When Habits Are Greener.", cls="text-success"), cls="display-4 fw-bolder text-center text-lg-start"),
                P("Sortify helps you sort waste smartly, turning small habits into big impacts for the environment. Earn points and redeem them for exciting rewards!", cls="lead text-muted my-4 text-center text-lg-start"),
                Div(
                    A("Start Sorting Now", href="/scan", cls="btn btn-success btn-lg px-4 me-sm-3 fw-bold", hx_get="/scan", hx_target="#mainContent"),
                    A("View Rewards", href="/reward", cls="btn btn-outline-secondary btn-lg px-4 mt-2 mt-sm-0", hx_get="/reward", hx_target="#mainContent"),
                    cls="d-grid gap-2 d-sm-flex justify-content-sm-center justify-content-lg-start"
                ),
                cls="col-lg-6 order-2 order-lg-1"
            ),
            Div(
                Img(src="/static/landing/hero-image.png", cls="img-fluid hero-image", alt="Hero Image"),
                cls="col-lg-6 order-1 order-lg-2"
            ),
            cls="row gx-5 align-items-center justify-content-center"
        ),
        cls="container px-5 py-5"
    )

def landing_stats():
    stats_data = [
        {"id": "stat-users", "value": "12,000+", "label": "Active Users"},
        {"id": "stat-sorted-waste", "value": "5 Tons", "label": "Sorted Waste"},
        {"id": "stat-rewards", "value": "100+", "label": "Rewards Redeemed"},
        {"id": "stat-joined-communities", "value": "45", "label": "Joined Communities"}
    ]
    
    def stat_item(data):
        return Div(
            Div(data["value"], id=data["id"], cls="display-4 fw-bold text-success"),
            Div(data["label"], cls="text-muted"),
            cls="text-center"
        )

    return Div(
        Div(
            Div(*[Div(stat_item(s), cls="col") for s in stats_data], cls="row row-cols-2 row-cols-lg-4 g-4"),
            cls="container px-5"
        ),
        cls="py-5 bg-success bg-opacity-10"
    )

def landing_features():
    features_data = [
        {
            "title": "Smart & Fast Scanning",
            "desc": "No more confusion. Just dispose your waste at sortify, and our system will instantly recognize its type and dispose it with proper sorting.",
            "img_src": "/static/landing/feature-scan.png"
        },
        {
            "title": "Point & Rewards System",
            "desc": "Every time you sort your waste correctly, you earn points. Collect as many points as possible and exchange them for vouchers, donations, or exclusive merchandise.",
            "img_src": "/static/landing/feature-reward.png"
        }
    ]
    
    def feature_item(data, reverse=False):
        img_col = Div(Img(src=data["img_src"], cls="img-fluid rounded-3"), cls="col-md-5")
        text_col = Div(
            H2(data["title"], cls="fw-bolder"),
            P(data["desc"], cls="lead text-muted"),
            cls="col-md-7"
        )
        
        order_img = "order-md-2" if reverse else ""
        order_text = "order-md-1" if reverse else ""
        
        return Div(
            Div(
                Div(img_col, cls=f"{order_img}"),
                Div(text_col, cls=f"{order_text}"),
                cls="row gx-5 align-items-center"
            ),
            cls="mb-5"
        )

    return Div(
        feature_item(features_data[0]),
        feature_item(features_data[1], reverse=True),
        cls="container px-5 my-5"
    )

def landing_process():
    process_data = [
        {"icon": "recycling", "title": "1. Dispose Waste", "desc": "Insert your trash into the Sortify machine."},
        {"icon": "inventory_2", "title": "2. Automatic Sorting", "desc": "Our smart system will automatically sort it."},
        {"icon": "military_tech", "title": "3. Earn Points", "desc": "You will earn points for every sorting."},
        {"icon": "redeem", "title": "4. Redeem Rewards", "desc": "Exchange points for various exciting prizes."}
    ]
    def process_card(data):
        return Div(
            Div(
                Div(Span(data["icon"], cls="material-symbols-rounded fs-1 text-white"), cls="feature bg-success bg-gradient text-white rounded-3 mb-3"),
                H2(data["title"], cls="fs-4 fw-bold"),
                P(data["desc"], cls="mb-0 text-muted"),
                cls="text-center"
            )
        )
    return Div(
        Div(
            Div(H2("Turn Waste into Rewards in 4 Easy Steps", cls="text-center fw-bolder mb-5")),
            Div(*[Div(process_card(p), cls="col-lg-3 col-md-6 mb-5 mb-lg-0") for p in process_data], cls="row gx-5"),
            cls="container px-5 my-5"
        )
    )

def landing_testimonials():
    testi_data = [
        {"quote": "Sortify completely changed the way I see trash. Now I'm excited to earn points!", "name": "Andi Wijaya", "title": "Student"},
        {"quote": "This app is very educational. My child has learned a lot about different types of waste.", "name": "Citra Lestari", "title": "Housewife"},
        {"quote": "As an environmental activist, I fully support initiatives like this. Awesome!", "name": "Budi Hartono", "title": "Environmental Activist"}
    ]
    
    def testi_card(data):
        return Div(
            Div(
                Div(Span("format_quote", cls="material-symbols-rounded fs-1 text-success"), cls="text-center mb-1"),
                P(f'"{data["quote"]}"', cls="mb-4 fst-italic"),
                Div(
                    Img(src="https://placehold.co/50x50/E2E8F0/475569?text=AV", cls="rounded-circle me-3"),
                    Div(
                        Div(data["name"], cls="fw-bold"),
                        Div(data["title"], cls="text-muted")
                    ),
                    cls="d-flex align-items-center justify-content-center"
                ),
                cls="card-body p-4"
            ),
            cls="card shadow-sm"
        )
    
    return Div(
        Div(
            Div(H2("What do they say about Sortify?", cls="text-center fw-bolder mb-5")),
            Div(*[Div(testi_card(t), cls="col-lg-4 mb-5 mb-lg-0") for t in testi_data], cls="row gx-5"),
            cls="container px-5 py-3 my-5"
        ),
        cls="bg-success bg-opacity-10"
    )

def landing_cta():
    return Div(
        Div(
            Div(
                H2("Ready to Make a Change?", cls="fw-bolder"),
                P("Join thousands of others who have become environmental heroes with Sortify.", cls="lead text-muted"),
                A("Sign Up Free", href="/register", cls="btn btn-lg btn-success fw-bold mt-3", hx_get="/register", hx_target="#mainContent"),
                cls="text-center"
            ),
            cls="container px-5"
        ),
        cls="py-5"
    )

def landing_section(user=None):
    return Div(
        ScrollTop(),
        landing_hero(),
        landing_stats(),
        landing_features(),
        landing_process(),
        landing_testimonials(),
        landing_cta() if user is None else None,
        ScrollTop(),
        cls="landing-page"
    )

def dashboard_header():
    return Div(
        Div(
            H1("Dashboard", cls="fw-bold mb-1"),
            P("Welcome back, here's your waste management overview.", cls="text-muted")
        ),
        cls="d-flex flex-column flex-sm-row justify-content-between align-items-sm-center mb-4"
    )

def time_ago(ts):
    try:
        t = datetime.fromisoformat(ts) if isinstance(ts, str) else ts
        delta = datetime.now() - t
        seconds = delta.total_seconds()
        if seconds < 60:
            return f"{int(seconds)} seconds ago"
        elif seconds < 3600:
            return f"{int(seconds // 60)} minutes ago"
        elif seconds < 86400:
            return f"{int(seconds // 3600)} hours ago"
        else:
            return f"{int(seconds // 86400)} days ago"
    except Exception:
        return "Unknown time"

def get_color(waste_type):
    mapping = {
        "Recycle": "primary",
        "Organic": "success",
        "Paper": "warning",
        "Others": "secondary"
    }
    return mapping.get(waste_type.capitalize(), "secondary")

def disposal_logs_card(logs):
    def log_row(log):
        username = log.username or "Unknown"
        initials = "".join([name[0] for name in username.split()[:2]]).upper()
        badge_class = f"badge text-bg-{get_color(log.waste_type)}"
        return Tr(
            Td(f"#{log.id}", cls="align-middle small text-muted"),
            Td(
                Div(
                    Img(src=f"https://placehold.co/32x32/E2E8F0/475569?text={initials}", alt=username, cls="rounded-circle me-3"),
                    Span(username, cls="fw-medium"),
                    cls="d-flex align-items-center"
                ),
                cls="align-middle"
            ),
            Td(Span(log.waste_type.capitalize(), cls=badge_class), cls="align-middle"),
            Td(time_ago(log.timestamp), cls="align-middle small text-muted"),
        )

    return Div(
        Div(
            H5("Disposal Logs", cls="card-title fw-bold"),
            A("View All", href="#", cls="btn-link text-decoration-none"),
            cls="d-flex justify-content-between align-items-center mb-3"
        ),
        Div(
            Table(
                Thead(
                    Tr(
                        Th("Dispose ID", scope="col"),
                        Th("User", scope="col"),
                        Th("Waste Type", scope="col"),
                        Th("Time", scope="col"),
                    )
                ),
                Tbody(*[log_row(log) for log in logs]),
                cls="table table-borderless table-hover"
            ),
            cls="table-responsive"
        ),
        cls="card-body"
    )

def weekly_disposal_card():
    return Div(
        H5("Weekly Disposal", cls="card-title fw-bold"),
        P("Number of disposals in the last 7 days.", cls="card-subtitle mb-4 text-muted"),
        Div(
            Canvas(id="weeklyDisposalChart"),
            style="height: 20rem;"
        ),
        cls="card-body"
    )

def leaderboard_card(leaders):
    def leader_item(leader, rank):
        initials = "".join([name[0] for name in leader.username.split()[:2]]).upper()
        return Div(
            Div(
                Img(src=f"https://placehold.co/40x40/E2E8F0/475569?text={initials}", alt=leader.username, cls="rounded-circle me-3"),
                Div(
                    P(leader.username, cls="fw-semibold mb-0"),
                    P(f"Rank {rank}", cls="small text-muted mb-0")
                ),
                cls="d-flex align-items-center"
            ),
            Span(f"{leader.point:,} pts", cls="fw-bold text-success"),
            cls="d-flex align-items-center justify-content-between"
        )

    return Div(
        Div(
            H5("Leaderboard", cls="card-title fw-bold"),
            A("See All", href="#", cls="btn-link text-decoration-none"),
            cls="d-flex justify-content-between align-items-center mb-3"
        ),
        Div(*[leader_item(leader, i + 1) for i, leader in enumerate(leaders)], cls="vstack gap-3"),
        cls="card-body"
    )

def bin_availability_card():
    waste_types = [
        {"name": "Paper", "percentage": "60%", "color": "warning"},
        {"name": "Recycle", "percentage": "80%", "color": "primary"},
        {"name": "Organic", "percentage": "90%", "color": "success"},
        {"name": "Others", "percentage": "70%", "color": "secondary"},
    ]

    def legend_item(item):
        return Div(
            Div(
                Span(cls=f"d-inline-block rounded-circle me-2 bg-{item['color']}", style="width: 0.75rem; height: 0.75rem;"),
                Span(item["name"]),
                cls="d-flex align-items-center"
            ),
            Span(item["percentage"], cls="fw-medium"),
            cls="d-flex justify-content-between align-items-center"
        )

    return Div(
        H5("Bin Availability", cls="card-title fw-bold mb-4"),
        Div(
            Canvas(id="binAvailabilityChart"),
            Div(
                H2("75%", cls="fw-bold"),
                P("Overall Full", cls="text-muted small"),
                cls="position-absolute top-50 start-50 translate-middle text-center"
            ),
            cls="position-relative mx-auto",
            style="height: 14rem; width: 14rem;"
        ),
        Div(*[legend_item(item) for item in waste_types], cls="vstack gap-2 mt-4"),
        cls="card-body"
    )

def charts_script(chart_labels, chart_data):
    return Script(f"""
        function initDashboardCharts() {{
            if (typeof Chart === 'undefined') return;

            if (window.weeklyChart instanceof Chart) window.weeklyChart.destroy();
            if (window.binChart instanceof Chart) window.binChart.destroy();

            const weeklyDisposalCtx = document.getElementById('weeklyDisposalChart')?.getContext('2d');
            if (weeklyDisposalCtx) {{
                const labels = {json.dumps(chart_labels)};
                const data = {json.dumps(chart_data)};

                window.weeklyChart = new Chart(weeklyDisposalCtx, {{
                    type: 'bar',
                    data: {{ labels, datasets: [{{ label: 'Disposals', data, backgroundColor: 'rgba(25,135,84,0.2)', borderColor: 'rgba(25,135,84,1)', borderWidth: 2, borderRadius: 8, barThickness: 20 }}] }},
                    options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }}, x: {{ grid: {{ display: false }} }} }} }}
                }});
            }}

            const binAvailabilityCtx = document.getElementById('binAvailabilityChart')?.getContext('2d');
            if (binAvailabilityCtx) {{
                window.binChart = new Chart(binAvailabilityCtx, {{
                    type: 'doughnut',
                    data: {{
                        labels: ['Paper', 'Recycle', 'Organic', 'Others'],
                        datasets: [{{
                            data: [60, 80, 90, 70],
                            backgroundColor: ['#FFC107', '#0D6EFD', '#198754', '#6C757D'],
                            borderColor: '#FFFFFF', borderWidth: 4, hoverOffset: 8
                        }}]
                    }},
                    options: {{ responsive: true, maintainAspectRatio: false, cutout: '75%', plugins: {{ legend: {{ display: false }}, tooltip: {{ enabled: false }} }} }}
                }});
            }}
        }}
        initDashboardCharts();
    """)

def dashboard_section():
    db = get_db_session()
    try:
        top_leaders = db.query(User).order_by(desc(User.point)).limit(5).all()

        today = datetime.now()
        seven_days_ago = today - timedelta(days=7)
        daily_counts = {(today - timedelta(days=i)).strftime('%a'): 0 for i in range(7)}
        day_labels = [(today - timedelta(days=i)).strftime('%a') for i in range(6, -1, -1)]

        logs = db.query(WasteDetectionLog).all()
        recent_logs = db.query(WasteDetectionLog).order_by(desc(WasteDetectionLog.timestamp)).limit(5).all()

        for log in logs:
            if not isinstance(log.timestamp, str):
                continue
            try:
                ts = datetime.fromisoformat(log.timestamp)
            except:
                continue
            if ts >= seven_days_ago:
                day_name = ts.strftime('%a')
                if day_name in daily_counts:
                    daily_counts[day_name] += 1

        final_chart_data = [daily_counts[day] for day in day_labels]

    finally:
        db.close()

    return Div(
        ScrollTop(),
        dashboard_header(),
        Div(
            Div(
                Div(weekly_disposal_card(), cls="card shadow-sm mb-4"),
                Div(disposal_logs_card(recent_logs), cls="card shadow-sm"),
                cls="col-lg-8"
            ),
            Div(
                Div(bin_availability_card(), cls="card shadow-sm mb-4"),
                Div(leaderboard_card(top_leaders), cls="card shadow-sm"),
                cls="col-lg-4"
            ),
            cls="row g-4"
        ),
        charts_script(day_labels, final_chart_data),
        cls="container-fluid p-4"
    )