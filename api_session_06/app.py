import os
import bcrypt
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from data import USERS, load_permissions, orders_by_owner

app = Flask(__name__)
app.json.ensure_ascii = False
app.json.sort_keys = False
app.config.update(
    SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "dev-flask-secret"),
    JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-demo"),
    JWT_ACCESS_TOKEN_EXPIRES=900,         
    JWT_REFRESH_TOKEN_EXPIRES=2592000,    
    JWT_ALGORITHM="HS256",
)
jwt = JWTManager(app)


# ___POST /api/auth/login___ cap access + refresh kem claims
@app.post("/api/auth/login")
def login():
    body = request.get_json(silent=True) or {}
    user = USERS.get(body.get("email"))
    pwd = body.get("password", "").encode()
    if not user or not bcrypt.checkpw(pwd, user["pwd_hash"]):
        return jsonify(error="invalid_credentials"), 401
    claims = load_permissions(user["id"])
    uid = str(user["id"])
    return jsonify(
        access=create_access_token(identity=uid, additional_claims=claims),
        refresh=create_refresh_token(identity=uid, additional_claims=claims),
    )


# ___GET /api/orders___ token + scope orders:read
@app.get("/api/orders")
@jwt_required()
def list_orders():
    uid = get_jwt_identity()
    claims = get_jwt()
    if "orders:read" not in claims.get("scopes", []):
        return jsonify(error="insufficient_scope"), 403
    return jsonify(orders_by_owner(uid))


# ___POST /api/auth/refresh___ refresh token lay access new
@app.post("/api/auth/refresh")
@jwt_required(refresh=True)
def refresh():
    claims = load_permissions(get_jwt_identity())
    return jsonify(access=create_access_token(
        identity=get_jwt_identity(), additional_claims=claims))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
