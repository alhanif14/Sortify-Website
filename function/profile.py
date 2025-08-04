from fasthtml.common import *
from datetime import datetime, timedelta

def time_ago(ts):
    if not ts: return "Unknown time"
    now = datetime.now(ts.tzinfo) if ts.tzinfo else datetime.now()
    delta = now - ts
    seconds = delta.total_seconds()
    if seconds < 60: return f"{int(seconds)}s ago"
    if seconds < 3600: return f"{int(seconds // 60)}m ago"
    if seconds < 86400: return f"{int(seconds // 3600)}h ago"
    return f"{int(seconds // 86400)}d ago"

def get_color(waste_type):
    mapping = {"Recycle": "primary", "Organic": "success", "Paper": "warning", "Other": "secondary"}
    return mapping.get(waste_type, "secondary")


def user_profile_card(user):
    initials = "".join([part[0] for part in user.username.split()[:2]]).upper()
    return Div(
        Div(
            Img(src=f"https://placehold.co/96x96/198754/FFFFFF?text={initials}", alt=user.username, cls="rounded-circle mb-3"),
            H4(user.username, cls="fw-bold"),
            P(user.email, cls="text-muted small"),
            cls="d-flex flex-column align-items-center text-center"
        ),
        Hr(),
        Div(
            Span("military_tech", cls="material-symbols-rounded text-success me-2"),
            Span(f"{user.point or 0:,} Points", cls="fs-5 fw-semibold"),
            cls="d-flex align-items-center mb-3"
        ),
        Button("Logout", cls="btn btn-outline-danger w-100", hx_post="/logout", hx_target="#mainContent", hx_confirm="Are you sure?"),
        cls="card-body d-flex flex-column"
    )

def user_disposal_logs_table(search=""):
    return Div(
        Div(id="user-logs-content", hx_get=f"/profile/logs?search={search}", hx_trigger="load",
            _=[P("Loading logs...", cls="text-center text-muted p-5")]),
        cls="card shadow-sm h-100"
    )

def user_disposal_logs_content(logs, page, total_pages, search, sort_by, order):
    def log_row(log):
        badge_class = f"badge text-bg-{get_color(log.waste_type)}"
        return Tr(Td(f"#{log.id}", cls="align-middle small text-muted"), Td(Span(log.waste_type.capitalize(), cls=badge_class), cls="align-middle"), Td(f"{log.point} pts", cls="align-middle fw-medium text-success"), Td(time_ago(log.timestamp), cls="align-middle small text-muted"))
    
    def sortable_th(label, column_name):
        is_active = sort_by == column_name
        next_order = "asc" if is_active and order == "desc" else "desc"
        icon_name = "arrow_downward" if is_active and order == "desc" else "arrow_upward" if is_active else "unfold_more"
        icon = I(icon_name, cls="material-symbols-rounded align-middle small")
        return Th(A(label, " ", icon, href="#", hx_get=f"/profile/logs?sort_by={column_name}&order={next_order}&search={search}", hx_target="#user-logs-content", cls="text-decoration-none text-dark"))

    return Div(
        Div(
            H5("Disposal History", cls="card-title fw-bold"),
            Form(Input(type="search", name="search", value=search, placeholder="Search by waste type...", cls="form-control form-control-sm", style="max-width: 250px;"), 
                 hx_get="/profile/logs", hx_trigger="submit, search", hx_target="#user-logs-content"),
            cls="d-flex justify-content-between align-items-center mb-3 p-3 border-bottom"
        ),
        Div(
            Table(Thead(Tr(sortable_th("ID", "id"), sortable_th("Waste Type", "waste_type"), sortable_th("Points", "point"), sortable_th("Time", "timestamp"))),
                  Tbody(*[log_row(log) for log in logs] if logs else Tr(Td("No logs found.", colspan="4", cls="text-center text-muted p-4"))),
                  cls="table table-hover mb-0"),
            cls="table-responsive"
        ),
        Nav(
            Ul(*[Li(A(str(p), href="#", hx_get=f"/profile/logs?page={p}&sort_by={sort_by}&order={order}&search={search}", hx_target="#user-logs-content", cls=f"page-link {'active' if p == page else ''}"), cls="page-item") for p in range(1, total_pages + 1)],
               cls="pagination pagination-sm justify-content-end mt-3 px-3")
        ) if total_pages > 1 else "",
        id="user-logs-content"
    )

def user_stats_summary(stats):
    
    stats_items = [
        {"label": "Recycle", "count": stats.get("Recycle", 0), "icon": "recycling", "color": "primary"},
        {"label": "Paper", "count": stats.get("Paper", 0), "icon": "article", "color": "warning"},
        {"label": "Organic", "count": stats.get("Organic", 0), "icon": "eco", "color": "success"},
        {"label": "Other", "count": stats.get("Other", 0), "icon": "delete_outline", "color": "secondary"},
    ]

    def stat_item(item):
        return Div(
            Div(
                Span(item["icon"], cls=f"material-symbols-rounded text-{item['color']} me-3"),
                Span(item["label"]),
                cls="d-flex align-items-center"
            ),
            Span(str(item["count"]), cls="fw-bold"),
            cls="d-flex justify-content-between align-items-center mb-3"
        )

    return Div(
        H5("Summary", cls="card-title fw-bold mb-3"),
        *[stat_item(item) for item in stats_items],
        cls="card-body"
    )

def profile_section(user, disposal_stats):
    return Div(
        Div(
            Div(
                Div(
                    Div(user_profile_card(user), cls="card shadow-sm mb-4"),
                    
                    Div(user_stats_summary(disposal_stats), cls="card shadow-sm"),
                    
                    cls="col-lg-3 mb-4 mb-lg-0"
                ),
                
                Div(
                    user_disposal_logs_table(),
                    cls="col-lg-9"
                ),
                cls="row"
            ),
            cls="container-fluid p-3 p-md-4"
        ),
        cls="profile-page"
    )