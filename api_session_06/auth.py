from functools import wraps
from flask import jsonify
from flask_jwt_extended import current_user, get_jwt
from data import ORDERS


# Decorator 1: roles (OR) - chi can co 1 role trong danh sach
def require_roles(*allowed):
    def d(fn):
        @wraps(fn)
        def w(*a, **kw):
            urs = set(current_user["roles"])
            if not urs & set(allowed):
                return jsonify({
                    "error": "forbidden",
                    "need_one_of": list(allowed)
                }), 403
            return fn(*a, **kw)
        return w
    return d


# Decorator 2: scopes (AND) - phai co du tat ca scope
def require_scopes(*needed):
    def d(fn):
        @wraps(fn)
        def w(*a, **kw):
            granted = set(get_jwt().get("scopes", []))
            if not set(needed).issubset(granted):
                return jsonify({
                    "error": "insufficient_scope",
                    "need_all_of": list(needed)
                }), 403
            return fn(*a, **kw)
        return w
    return d


# Decorator 3: ownership - chong BOLA, chi chu order (hoac admin) moi duoc dung
def user_owns_resource(param="id"):
    def d(fn):
        @wraps(fn)
        def w(*a, **kw):
            row = ORDERS.get(kw[param])
            if not row:
                return jsonify({"error": "not_found"}), 404
            ok = str(row["owner_id"]) == str(current_user["id"])
            if not ok and "admin" not in current_user["roles"]:
                return jsonify({"error": "forbidden"}), 403
            return fn(*a, **kw)
        return w
    return d
