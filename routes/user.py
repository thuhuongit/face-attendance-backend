from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import User

user_bp = Blueprint('user_bp', __name__)

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
            salary_rate=float(data.get('salary_rate', 0.0))
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created', 'user': user.to_dict()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Email đã tồn tại!'}), 400

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
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})
