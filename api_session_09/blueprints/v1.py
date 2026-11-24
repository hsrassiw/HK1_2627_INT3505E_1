from datetime import datetime, timezone
from flask import Blueprint
from sunset import deprecate_at
from .users_data import get_user

bp = Blueprint("v1", __name__)

V1_SUNSET = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

@bp.route("/users/<int:uid>")
@deprecate_at(V1_SUNSET, replacement="/api/v2/users")
def get(uid):
    u = get_user(uid)
    if not u:
        return {"error": "nf"}, 404
    return {
        "id": uid,
        "full_name": f"{u['first_name']} {u['last_name']}",
        "email": u["email"],
    }