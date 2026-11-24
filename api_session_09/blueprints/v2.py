from flask import Blueprint, request
from .users_data import get_user, create_user

bp = Blueprint("v2", __name__)

@bp.route("/users/<int:uid>")
def get(uid):
    u = get_user(uid)
    if not u:
        return {"error": "nf"}, 404
    return {
        "id": uid,
        "first_name": u["first_name"],
        "last_name": u["last_name"],
        "email": u["email"],
    }

@bp.route("/users", methods=["POST"])
def create():
    data = request.get_json(silent=True) or {}
    missing = [f for f in ("first_name", "last_name", "email") if not data.get(f)]
    if missing:
        return {"error": "missing fields", "fields": missing}, 400
    return create_user(data["first_name"], data["last_name"], data["email"]), 201
