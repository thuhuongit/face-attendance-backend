# routes/attendance.py

from flask import Blueprint, request, jsonify
from extensions import db
from models import AttendanceLog, User
from datetime import datetime
from utils.mail import send_email  # nếu bạn có hàm gửi mail

attendance_bp = Blueprint("attendance_bp", __name__)

@attendance_bp.route("/api/attendance/checkin", methods=["POST"])
def check_in():
    data = request.get_json()
    user_id = data.get("user_id")

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    log = AttendanceLog(user_id=user_id, check_in_time=datetime.utcnow())
    db.session.add(log)
    db.session.commit()

    # Gửi mail xác nhận (tùy chọn)
    send_email(user.email, "Check-in thành công", f"Bạn đã check-in lúc {log.check_in_time.strftime('%H:%M:%S')}.")

    return jsonify({"message": "Check-in thành công"})

@attendance_bp.route("/api/attendance/checkout", methods=["POST"])
def check_out():
    data = request.get_json()
    user_id = data.get("user_id")

    log = AttendanceLog.query.filter_by(user_id=user_id, check_out_time=None).order_by(AttendanceLog.check_in_time.desc()).first()

    if not log:
        return jsonify({"message": "Không tìm thấy log check-in chưa check-out"}), 404

    log.check_out_time = datetime.utcnow()

    # Tính giờ công và lương
    duration = (log.check_out_time - log.check_in_time).seconds / 3600  # giờ
    rate = 50000  # giả sử 50k/giờ
    log.salary = round(duration * rate, 2)

    db.session.commit()

    # Gửi mail xác nhận
    send_email(log.user.email, "Check-out thành công", f"Bạn đã check-out lúc {log.check_out_time.strftime('%H:%M:%S')}. Lương tạm tính: {log.salary} VNĐ.")

    return jsonify({"message": "Check-out thành công", "salary": log.salary})
