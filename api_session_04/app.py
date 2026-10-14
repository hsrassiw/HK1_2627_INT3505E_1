import os

import yaml
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.json.ensure_ascii = False
app.json.sort_keys = False
BASE = "/BookStore/1.0.0"

SPEC_FILE = os.path.join(os.path.dirname(__file__), "Bookstore.yaml")
with open(SPEC_FILE, encoding="utf-8") as f:
    SPEC = yaml.safe_load(f)

FIELDS = ["name", "category", "status"]
STATUSES = ["available", "pending", "sold"]
_next = 2
BOOKS = [
    {"id": 1, "name": "Data, Structure and Algorithm", "category": "Textbook", "status": "available"},
]


def bad_request(msg):
    return jsonify(error_code="INVALID_INPUT", message=msg), 400


def not_found():
    return jsonify(error_code="NOT_FOUND", message="Không tìm thấy dữ liệu yêu cầu."), 404


@app.errorhandler(HTTPException)
def handle_http(e):
    if e.code == 404:
        return not_found()
    return jsonify(error_code=e.name.upper().replace(" ", "_"), message=e.description), e.code


def parse_id(raw):
    if not raw.isdecimal() or int(raw) <= 0:
        return None
    return int(raw)


def find(bid):
    for b in BOOKS:
        if b["id"] == bid:
            return b
    return None


def validate(data, partial=False):
    if not isinstance(data, dict):
        return "Body phải là JSON object."
    if not partial and "name" not in data:
        return "Thiếu trường bắt buộc 'name'."
    if not partial and "id" in data and (not isinstance(data["id"], int) or isinstance(data["id"], bool)):
        return "Trường 'id' phải là số nguyên."
    for f in FIELDS:
        if f in data and not isinstance(data[f], str):
            return f"Trường '{f}' phải là chuỗi."
    if "name" in data and not data["name"].strip():
        return "Trường 'name' không được rỗng."
    if "status" in data and data["status"] not in STATUSES:
        return f"Trường 'status' phải là một trong {STATUSES}."
    return None


def make_book(bid, data):
    book = {"id": bid, "name": data["name"].strip()}
    for f in ["category", "status"]:
        if f in data:
            book[f] = data[f]
    return book


# ___GET /books___
@app.get(f"{BASE}/books")
def get_books():
    return jsonify(BOOKS), 200


# ___POST /books___
@app.post(f"{BASE}/books")
def create_book():
    global _next
    data = request.get_json(silent=True)
    err = validate(data)
    if err:
        return bad_request(err)
    book = make_book(_next, data)
    _next += 1
    BOOKS.append(book)
    return jsonify(book), 201


# ___GET /books/<book_id>___
@app.get(f"{BASE}/books/<book_id>")
def get_book(book_id):
    bid = parse_id(book_id)
    if bid is None:
        return bad_request("ID phải là một số nguyên dương.")
    book = find(bid)
    if book is None:
        return not_found()
    return jsonify(book), 200


# ___PUT /books/<book_id>___
@app.put(f"{BASE}/books/<book_id>")
def update_book(book_id):
    bid = parse_id(book_id)
    if bid is None:
        return bad_request("ID phải là một số nguyên dương.")
    book = find(bid)
    if book is None:
        return not_found()
    data = request.get_json(silent=True)
    err = validate(data)
    if err:
        return bad_request(err)
    new_book = make_book(bid, data)
    BOOKS[BOOKS.index(book)] = new_book
    return jsonify(new_book), 200


# ___PATCH /books/<book_id>___
@app.patch(f"{BASE}/books/<book_id>")
def modify_book(book_id):
    bid = parse_id(book_id)
    if bid is None:
        return bad_request("ID phải là một số nguyên dương.")
    book = find(bid)
    if book is None:
        return not_found()
    data = request.get_json(silent=True)
    err = validate(data, partial=True)
    if err:
        return bad_request(err)
    for f in FIELDS:
        if f in data:
            book[f] = data[f].strip() if f == "name" else data[f]
    return jsonify(book), 200


# ___DELETE /books/<book_id>___
@app.delete(f"{BASE}/books/<book_id>")
def delete_book(book_id):
    bid = parse_id(book_id)
    if bid is None:
        return bad_request("ID phải là một số nguyên dương.")
    book = find(bid)
    if book is None:
        return not_found()
    BOOKS.remove(book)
    return "", 204


# ___GET /openapi.json___ tra spec, them server local len dau de Try it out goi ve may nay
@app.get("/openapi.json")
def openapi_json():
    spec = dict(SPEC)
    spec["servers"] = [{"url": BASE, "description": "Local"}] + SPEC.get("servers", [])
    return jsonify(spec)


# ___GET /docs___ Swagger UI (lay tu CDN), doc spec tu /openapi.json
SWAGGER_HTML = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>BookStore - Swagger UI</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({url: "/openapi.json", dom_id: "#swagger-ui"});
  </script>
</body>
</html>"""


@app.get("/docs")
def docs():
    return SWAGGER_HTML


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
