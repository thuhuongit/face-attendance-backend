from flask import Blueprint, request, jsonify
from models import db, AttendanceLog, User
from datetime import datetime
from utils.mail_utils import send_attendance_email

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route("/attendance", methods=["POST"])
def mark_attendance():
    data = request.json
    user_id = data.get("user_id")
    check_type = data.get("check_type")  # 'in' hoặc 'out'

    if not user_id or check_type not in ['in', 'out']:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Không tìm thấy người dùng"}), 404

    now = datetime.now()

    log = AttendanceLog(user_id=user_id, check_type=check_type, timestamp=now)
    db.session.add(log)
    db.session.commit()

    send_attendance_email(user.email, user.name, now.strftime("%H:%M %d/%m/%Y"))

    return jsonify({"message": "Điểm danh thành công và đã gửi email!"})
