from flask import Flask, jsonify, request

app = Flask(__name__)
_next = 3
POSTS = [
    {"id": 1, "user_id": 1, "title": "Bai1", "content": "ND1", "tags": ["flask"]},
    {"id": 2, "user_id": 2, "title": "Bai2", "content": "ND2", "tags": ["api"]},
]


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


# ___POST /api/v1/posts___ tao bai viet moi
@app.post("/api/v1/posts")
def create_post():
    global _next
    p = request.get_json(silent=True) or {}
    t = (p.get("title") or "").strip()
    c = (p.get("content") or "").strip()
    if not t or not c:
        return jsonify(error="title and content required"), 422
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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
