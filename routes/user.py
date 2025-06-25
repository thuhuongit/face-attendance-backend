from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

# Tạo danh sách 
@user_bp.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    user = User(
        full_name=data['full_name'],
        email=data['email'],
        password=hashed_password,
        role=data.get('role', 'employee'),
        avatar=data.get('avatar', ''),
        salary_rate = float(data.get('salary_rate', 0.0))

    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

#Lấy danh sách 
@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    user.full_name = data.get('full_name', user.full_name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    if data.get('password'):
        user.password = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify({'message': 'User updated'})\
    
# Xóa danh sách 
@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})
