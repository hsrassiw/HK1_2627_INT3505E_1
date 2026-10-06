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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
