from fasthtml.common import *
from function.reward import reward_section, admin_reward_form, reward_unauthenticated_section
from database.database import get_current_user, get_db_session
from database.models import Voucher, UserVoucherRedeem, User
from starlette.requests import Request
from starlette.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import date

def reward_routes(rt):
    def is_admin(u):
        return u and u.email == "sortify01@gmail.com"
    def get_categorized_vouchers(db: Session, user: User):
        redeemed_vouchers_map = {r.voucher_id: r.redeem_date for r in db.query(UserVoucherRedeem).filter_by(user_id=user.id).all()}
        all_vouchers = db.query(Voucher).filter(Voucher.is_active == True).order_by(Voucher.point_cost).all()
        today = date.today()
        available, coming_soon, past = [], [], []
        for v in all_vouchers:
            if v.id in redeemed_vouchers_map:
                v.status_text = f"Redeemed on {redeemed_vouchers_map[v.id].strftime('%d %b %Y')}"
                past.append(v)
            elif v.end_date < today:
                v.status_text = f"Expired on {v.end_date.strftime('%d %b %Y')}"
                past.append(v)
            elif v.start_date > today:
                v.status_text = f"Available from {v.start_date.strftime('%d %b %Y')}"
                coming_soon.append(v)
            else:
                available.append(v)
        return available, coming_soon, past

    @rt("/reward")
    def get_reward_page(request: Request):
        user = get_current_user(request)
        if not user:
            return reward_unauthenticated_section()

        db: Session = get_db_session()
        try:
            available, coming_soon, past = get_categorized_vouchers(db, user)
            return reward_section(user, available, coming_soon, past)
        finally:
            db.close()

    @rt("/redeem/{voucher_id}")
    async def redeem_voucher(request: Request, voucher_id: int):
        user = get_current_user(request)
        if not user:
            return HTMLResponse("Session expired, please log in again.", status_code=401)

        db: Session = get_db_session()
        try:
            voucher = db.query(Voucher).filter(Voucher.id == voucher_id).first()
            if not voucher or user.point < voucher.point_cost or db.query(UserVoucherRedeem).filter_by(user_id=user.id, voucher_id=voucher.id).first():
                return HTMLResponse("Failed to redeem voucher.", status_code=400)

            user_in_db = db.query(User).filter(User.id == user.id).one()
            user_in_db.point -= voucher.point_cost
            new_redeem = UserVoucherRedeem(user_id=user.id, voucher_id=voucher.id)
            db.add(new_redeem)
            db.commit()
            db.refresh(user_in_db)

            available, coming_soon, past = get_categorized_vouchers(db, user_in_db)

            success_msg = f"Congratulations! You have successfully redeemed '{voucher.title}'."

            return reward_section(
                user=user_in_db, 
                available_vouchers=available,
                coming_soon_vouchers=coming_soon,
                past_vouchers=past,
                success_message=success_msg
            )
        except Exception as e:
            db.rollback()
            print(f"Error redeeming voucher: {e}")
            return HTMLResponse("There was an internal error.", status_code=500)
        finally:
            db.close()

    @rt("/admin/voucher/form")
    @rt("/admin/voucher/form/{voucher_id}")
    def get_voucher_form(request: Request, voucher_id: int = None):
        user = get_current_user(request)
        if not is_admin(user): return HTMLResponse("Forbidden", status_code=403)
        
        voucher = None
        if voucher_id:
            db: Session = get_db_session()
            voucher = db.query(Voucher).filter_by(id=voucher_id).first()
            db.close()
        
        form_component = admin_reward_form(voucher)
        
        title = "Edit Reward" if voucher else "Add New Reward"
        return Group(
            H5(title, cls="modal-title", hx_swap_oob="true:#adminRewardModal .modal-title"),
            form_component
        )

    @rt("/admin/voucher/save")
    async def save_voucher(request: Request):
        user = get_current_user(request)
        if not is_admin(user): return HTMLResponse("Forbidden", status_code=403)
        
        data = await request.form()
        voucher_id = data.get("voucher_id")
        
        db: Session = get_db_session()
        try:
            if voucher_id: # Mode Edit
                voucher = db.query(Voucher).filter_by(id=voucher_id).one()
            else: # Mode Add
                voucher = Voucher()
                db.add(voucher)
            
            voucher.title = data.get("title")
            voucher.description = data.get("description")
            voucher.point_cost = int(data.get("point_cost"))
            voucher.start_date = date.fromisoformat(data.get("start_date"))
            voucher.end_date = date.fromisoformat(data.get("end_date"))
            voucher.terms_conditions = data.get("terms_conditions")
            
            db.commit()

            available, coming_soon, past = get_categorized_vouchers(db, user)
            return reward_section(
                user=user, 
                available_vouchers=available,
                coming_soon_vouchers=coming_soon,
                past_vouchers=past,
                success_message=f"Voucher '{voucher.title}' has been saved."
            )
        except Exception as e:
            db.rollback()
            print(f"Admin save error: {e}")
            return HTMLResponse(f"Error saving voucher: {e}", status_code=500)
        finally:
            db.close()