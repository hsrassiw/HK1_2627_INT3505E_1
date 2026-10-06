import base64
import json
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from errors import ApiProblem, _problem

app = Flask(__name__)
_next = 3
POSTS = [
    {"id": 1, "user_id": 1, "title": "Bai1", "content": "ND1", "tags": ["flask"]},
    {"id": 2, "user_id": 2, "title": "Bai2", "content": "ND2", "tags": ["api"]},
]


def find(pid):
    for p in POSTS:
        if p["id"] == pid:
            return p
    return None


# ___Error handler___ tra ve problem+json
@app.errorhandler(ApiProblem)
def handle_problem(e):
    return _problem(e.status, e.title, e.detail, e.type_path, **e.extra)


@app.errorhandler(HTTPException)
def handle_http(e):
    return _problem(e.code, e.name, e.description)


@app.errorhandler(Exception)
def handle_500(e):
    app.logger.exception(e)
    return _problem(500, "Internal Server Error", "Server gap loi, vui long thu lai sau")


# ___GET /api/v1/posts___ lay danh sach, loc theo user_id va tag
@app.get("/api/v1/posts")
def list_posts():
    items = POSTS
    uid = request.args.get("user_id")
    if uid:
        items = [p for p in items if str(p["user_id"]) == uid]
    tag = request.args.get("tag")
    if tag:
        items = [p for p in items if tag in p["tags"]]
    return jsonify(items), 200


# ___GET /api/v1/posts/<id>___ xem chi tiet
@app.get("/api/v1/posts/<int:pid>")
def get_post(pid):
    post = find(pid)
    if post is None:
        raise ApiProblem(
            status=404,
            title="Post not found",
            detail=f"Khong tim thay bai viet id={pid}",
            type_path="post-not-found",
            resource_id=pid,
        )
    return jsonify(post), 200


# ___POST /api/v1/posts___ tao bai viet moi
@app.post("/api/v1/posts")
def create_post():
    global _next
    p = request.get_json() or {}
    t = (p.get("title") or "").strip()
    c = (p.get("content") or "").strip()
    if not t or not c:
        raise ApiProblem(
            status=422,
            title="Validation error",
            detail="title and content required",
            type_path="validation-error",
        )
    post = {
        "id": _next,
        "user_id": p.get("user_id", 1),
        "title": t,
        "content": c,
        "tags": p.get("tags", []),
    }
    _next += 1
    POSTS.append(post)
    return post, 201, {"Location": f"/api/v1/posts/{post['id']}"}


# ___GET /api/v1/test-error___ thu loi 500
@app.get("/api/v1/test-error")
def test_error():
    return 1 / 0


# ___LAB 3: /api/v1/orders___
STATUSES = ["pending", "paid", "shipped", "cancelled"]
ORDERS = [
    {
        "id": i,
        "customer_id": i % 5 + 1,
        "status": STATUSES[i % 4],
        "total": (i * 37) % 500 + 10,
        "created_at": f"2026-09-{i:02d}",
    }
    for i in range(1, 26)
]
FIELDS = ["id", "customer_id", "status", "total", "created_at"]
SORTS = ["id", "total", "created_at"]


def bad_param(msg):
    return ApiProblem(400, "Invalid parameter", msg, "invalid-parameter")


# cursor = base64 cua {"id": id don cuoi trang truoc}
def encode_cursor(oid):
    raw = json.dumps({"id": oid})
    return base64.urlsafe_b64encode(raw.encode()).decode()


def decode_cursor(c):
    try:
        return json.loads(base64.urlsafe_b64decode(c))["id"]
    except Exception:
        raise ApiProblem(400, "Invalid cursor", "cursor khong hop le", "invalid-cursor")


# ___GET /api/v1/orders___ cursor + filter + sort + fields
@app.get("/api/v1/orders")
def list_orders():
    a = request.args

    try:
        limit = int(a.get("limit", 10))
    except ValueError:
        raise bad_param("limit phai la so nguyen")
    limit = max(1, min(limit, 100))

    items = ORDERS
    if a.get("status"):
        items = [o for o in items if o["status"] == a["status"]]
    if a.get("customer_id"):
        items = [o for o in items if str(o["customer_id"]) == a["customer_id"]]

    sort = a.get("sort", "id")
    key = sort.lstrip("-")
    if key not in SORTS:
        raise bad_param(f"khong sort duoc theo {key}")
    items = sorted(items, key=lambda o: o[key], reverse=sort.startswith("-"))

    start = 0
    if a.get("cursor"):
        last_id = decode_cursor(a["cursor"])
        ids = [o["id"] for o in items]
        if last_id not in ids:
            raise ApiProblem(400, "Invalid cursor", "cursor khong hop le", "invalid-cursor")
        start = ids.index(last_id) + 1

    page = items[start:start + limit]
    next_cursor = None
    if start + limit < len(items):
        next_cursor = encode_cursor(page[-1]["id"])

    if a.get("fields"):
        fields = a["fields"].split(",")
        for f in fields:
            if f not in FIELDS:
                raise bad_param(f"field {f} khong ton tai")
        page = [{f: o[f] for f in fields} for o in page]

    return jsonify(data=page, next_cursor=next_cursor), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
