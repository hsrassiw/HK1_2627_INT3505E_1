from datetime import datetime, timezone
from functools import wraps
from flask import Flask, jsonify, request
from blueprints.v1 import bp as v1_bp
from blueprints.v2 import bp as v2_bp
from blueprints.users_data import get_user
from sunset import deprecate_at

LATEST = "2"
SUPPORTED = {"1", "2", "2024-06-20"}

app = Flask(__name__)
app.register_blueprint(v1_bp, url_prefix="/api/v1")
app.register_blueprint(v2_bp, url_prefix="/api/v2")


def api_version(supported=SUPPORTED, default=LATEST):
    def decorate(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            v = request.headers.get("X-API-Version", default)
            if v not in supported:
                return jsonify(error="unsupported version"), 400
            body, status = fn(v, *args, **kwargs)
            response = jsonify(body)
            response.status_code = status
            response.headers["X-API-Version-Served"] = v
            return response
        return wrapper
    return decorate


@app.route("/users/<int:uid>")
@api_version()
def get_user_by_header(version, uid):
    u = get_user(uid)
    if not u:
        return {"error": "not found"}, 404
    if version == "1":
        return {"id": uid, "full_name": f"{u['first_name']} {u['last_name']}"}, 200
    return {"id": uid, "first_name": u["first_name"],
            "last_name": u["last_name"], "email": u["email"]}, 200


@app.route("/api/v0/users/<int:uid>")
@deprecate_at(datetime(2026, 1, 1, tzinfo=timezone.utc), replacement="/api/v2/users")
def get_v0(uid):
    return {"id": uid}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
