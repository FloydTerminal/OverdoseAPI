from flask import Blueprint, jsonify, request # type: ignore
from app.models import db, User
from app.schemas.user_schemas import UserRequest
from datetime import datetime

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@users_bp.route('/', methods=['POST'])
def create_or_update_user():
    data = request.json
    user_data = UserRequest(**data)

    user = User.query.filter_by(user_id=user_data.user_id).first()
    if user:
        user.username = user_data.username
        user.discord_id = user_data.discord_id
        user.platform = user_data.platform
        user.last_login = datetime.utcnow()
    else:
        user = User(
            user_id=user_data.user_id,
            username=user_data.username,
            discord_id=user_data.discord_id,
            platform=user_data.platform,
            last_login=datetime.utcnow()
        )
        db.session.add(user)
    
    db.session.commit()
    return jsonify(user.to_dict()), 200

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
