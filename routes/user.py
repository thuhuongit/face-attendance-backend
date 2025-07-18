import os
import time
from flask import current_app
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import User
from models import AttendanceLog


user_bp = Blueprint('user_bp', __name__)



@user_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Sai thông tin đăng nhập'}), 401

    # Giả sử dùng JWT hoặc chỉ trả dữ liệu user (tuỳ mức độ bảo mật)
    return jsonify({
        'message': 'Đăng nhập thành công',
        'user': user.to_dict(),
        'token': 'dummy-token'  # hoặc dùng JWT thực
    })
 
# Lấy danh sách tất cả user
@user_bp.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

# Tạo user mới
@user_bp.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        hashed_password = generate_password_hash(data['password'])
        user = User(
            full_name=data['full_name'],
            email=data['email'],
            password=hashed_password,
            role=data.get('role', 'employee'),
            avatar=data.get('avatar', ''),
            salary_rate=float(data.get('salary_rate', 0.0)),
            employee_code=data.get('employee_code', ''),
            gender=data.get('gender', ''),
            dob=data.get('dob', None),
            birth_place=data.get('birth_place', ''),
            status=data.get('status', '')
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created', 'user': user.to_dict()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Email đã tồn tại!'}), 400
    
#Upload ảnh   
@user_bp.route('/api/upload-avatar', methods=['POST'])
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    filename = f"avatar_{int(time.time())}_{file.filename}"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    url = f"/static/avatars/{filename}"  # hoặc đường dẫn public của bạn
    return jsonify({'url': url})

# Cập nhật user theo ID
@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    user.full_name = data.get('full_name', user.full_name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    user.salary_rate = float(data.get('salary_rate', user.salary_rate))

    if data.get('password'):
        user.password = generate_password_hash(data['password'])

    db.session.commit()
    return jsonify({'message': 'User updated', 'user': user.to_dict()})

# Xóa user theo ID
@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Xoá attendance logs trước
    AttendanceLog.query.filter_by(user_id=user_id).delete()

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})


# Lấy thông tin chi tiết user theo ID
@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_detail(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.to_dict())