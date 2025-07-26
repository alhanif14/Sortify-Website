from fasthtml.common import *
from function.reward import reward_section, redeem_alert
from database.database import get_current_user, get_db_session
from database.models import Voucher, UserVoucherRedeem, User
from starlette.requests import Request
from starlette.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import date

def reward_routes(rt):
    @rt("/reward")
    def get_reward_page(request: Request):
        user = get_current_user(request)
        if not user:
            return HTMLResponse("You must be logged in to access this page.", status_code=401)

        db: Session = get_db_session()
        try:
            redeemed_voucher_ids = db.query(UserVoucherRedeem.voucher_id).filter(UserVoucherRedeem.user_id == user.id).all()
            redeemed_ids = {r_id for (r_id,) in redeemed_voucher_ids}
            today = date.today()
            active_vouchers = db.query(Voucher).filter(
                Voucher.is_active == True,
                Voucher.start_date <= today,
                Voucher.end_date >= today
            ).all()
            available_vouchers = [v for v in active_vouchers if v.id not in redeemed_ids]
            
            return reward_section(user, available_vouchers)
        finally:
            db.close()

    @rt("/redeem/{voucher_id}")
    async def redeem_voucher(request: Request, voucher_id: int):
        user = get_current_user(request)
        if not user:
            return redeem_alert("You must be logged in to redeem.", "danger")

        db: Session = get_db_session()
        try:
            voucher = db.query(Voucher).filter(Voucher.id == voucher_id).first()
            if not voucher or user.point < voucher.point_cost or db.query(UserVoucherRedeem).filter_by(user_id=user.id, voucher_id=voucher.id).first():
                return redeem_alert("Redeem failed: not enough points or already redeemed.", "danger")

            user_in_db = db.query(User).filter(User.id == user.id).one()
            user_in_db.point -= voucher.point_cost
            new_redeem = UserVoucherRedeem(user_id=user.id, voucher_id=voucher.id)
            db.add(new_redeem)
            db.commit()
            db.refresh(user_in_db)

            redeemed_voucher_ids = db.query(UserVoucherRedeem.voucher_id).filter(UserVoucherRedeem.user_id == user.id).all()
            redeemed_ids = {r_id for (r_id,) in redeemed_voucher_ids}
            today = date.today()
            active_vouchers = db.query(Voucher).filter(
                Voucher.is_active == True,
                Voucher.start_date <= today,
                Voucher.end_date >= today
            ).all()
            new_available_vouchers = [v for v in active_vouchers if v.id not in redeemed_ids]

            success_msg = f"Congratulations! You have successfully redeemed '{voucher.title}'."
            return reward_section(
            user=user_in_db, 
            available_vouchers=new_available_vouchers,
            success_message=success_msg
        )

        except Exception as e:
            db.rollback()
            print(f"Error redeeming voucher: {e}")
            return Div("An error occurred.", id="reward-section")
        finally:
            db.close()