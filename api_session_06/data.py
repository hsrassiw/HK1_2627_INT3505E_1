import bcrypt

USERS = {
    "an@vnu.edu.vn": {
        "id": 1,
        "pwd_hash": bcrypt.hashpw(b"secret123", bcrypt.gensalt()),
        "roles": ["manager"],
        "scopes": ["orders:read", "orders:write"],
    },
    "binh@vnu.edu.vn": {
        "id": 2,
        "pwd_hash": bcrypt.hashpw(b"secret123", bcrypt.gensalt()),
        "roles": ["manager"],
        "scopes": ["orders:read", "orders:write"],
    },
    # test 403
    "chi@vnu.edu.vn": {
        "id": 3,
        "pwd_hash": bcrypt.hashpw(b"secret123", bcrypt.gensalt()),
        "roles": ["viewer"],
        "scopes": [],
    },
}

ORDERS = {
    1: {"id": 1, "owner_id": 1, "item": "Clean Code"},
    2: {"id": 2, "owner_id": 2, "item": "Refactoring"},
    3: {"id": 3, "owner_id": 1, "item": "Mat biec"},
}


def find_user(uid):
    for u in USERS.values():
        if str(u["id"]) == str(uid):
            return u
    return None


def load_permissions(uid):
    u = find_user(uid)
    return {"roles": u["roles"], "scopes": u["scopes"]}


def orders_by_owner(uid):
    return [o for o in ORDERS.values() if str(o["owner_id"]) == str(uid)]
