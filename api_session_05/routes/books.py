import base64
import json
import os
from flask import Blueprint, abort, jsonify, request
from jsonschema import ValidationError, validate
from sqlalchemy import select, tuple_
from models import Author, Book, BookAuthor, db

bp = Blueprint("books", __name__, url_prefix="/api/v1/books")

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "..", "schemas", "book.json")
with open(SCHEMA_FILE, encoding="utf-8") as f:
    SCHEMA = json.load(f)


def check_body(payload):
    try:
        validate(payload, SCHEMA)
    except ValidationError as e:
        return jsonify(error="validation_failed", field=list(e.path), message=e.message), 400
    return None


# ___LAB 2___ sort + filter + cursor
# chi cho sort theo cac cot trong whitelist
SORT = {"id": Book.id, "price": Book.price_vnd}


def parse_sort(raw):
    desc = raw.startswith("-")
    key = raw.lstrip("-")
    if key not in SORT:
        return None, None, desc
    p = SORT[key]
    # sort them theo id de 2 sach cung gia van co thu tu co dinh
    cols = [
        p.desc() if desc else p.asc(),
        Book.id.desc() if desc else Book.id.asc(),
    ]
    return p, cols, desc


def _enc(s):
    return base64.urlsafe_b64encode(json.dumps(s).encode()).decode().rstrip("=")


# cursor = {"s": sort, "v": gia tri sort cua sach cuoi, "i": id sach cuoi}
def apply_cursor(q, raw, sort, p, desc):
    if not raw:
        return q, None
    try:
        pad = "=" * (-len(raw) % 4)
        c = json.loads(base64.urlsafe_b64decode(raw + pad))
        v, i = c["v"], c["i"]
    except Exception:
        return None, "bad_cursor"
    if c.get("s") != sort:
        return None, "sort_changed"
    if desc:
        cond = tuple_(p, Book.id) < tuple_(v, i)
    else:
        cond = tuple_(p, Book.id) > tuple_(v, i)
    return q.where(cond), None


def build_response(items, sort, p, more):
    nxt = None
    if items and more:
        last = items[-1]
        nxt = _enc({"s": sort, "v": getattr(last, p.key), "i": last.id})
    return jsonify(data=[b.to_dict() for b in items], page={"next": nxt, "more": more}), 200


# ___GET /api/v1/books___ lay danh sach sach
@bp.get("")
def list_books():
    raw = request.args.get("cursor")
    lim = max(1, min(request.args.get("limit", 20, type=int), 100))
    sort = request.args.get("sort", "-id")
    cat = request.args.get("category", type=int)

    p, cols, desc = parse_sort(sort)
    if p is None:
        return jsonify(error="bad_sort", message=f"khong sort duoc theo {sort}"), 400
    q = select(Book).order_by(*cols)
    if cat:
        q = q.where(Book.category_id == cat)
    q, err = apply_cursor(q, raw, sort, p, desc)
    if err:
        return jsonify(error=err, message="cursor khong hop le"), 400

    # lay du 1 dong de biet con trang sau khong
    rows = db.session.scalars(q.limit(lim + 1)).all()
    return build_response(rows[:lim], sort, p, len(rows) > lim)


# ___GET /api/v1/books/<id>___ xem chi tiet
@bp.get("/<int:bid>")
def get_book(bid):
    book = db.get_or_404(Book, bid)
    return jsonify(book.to_dict()), 200


# ___POST /api/v1/books___ tao sach moi
@bp.post("")
def create_book():
    payload = request.get_json(silent=True)
    err = check_body(payload)
    if err:
        return err
    book = Book(
        title=payload["title"],
        isbn=payload.get("isbn"),
        price_vnd=payload["price_vnd"],
        stock=payload.get("stock", 0),
        category_id=payload.get("category_id"),
    )
    db.session.add(book)
    db.session.commit()
    return book.to_dict(), 201, {"Location": f"/api/v1/books/{book.id}"}


# ___PUT /api/v1/books/<id>___ sua toan bo
@bp.put("/<int:bid>")
def update_book(bid):
    book = db.get_or_404(Book, bid)
    payload = request.get_json(silent=True)
    err = check_body(payload)
    if err:
        return err
    book.title = payload["title"]
    book.isbn = payload.get("isbn")
    book.price_vnd = payload["price_vnd"]
    book.stock = payload.get("stock", 0)
    book.category_id = payload.get("category_id")
    db.session.commit()
    return book.to_dict(), 200


# ___DELETE /api/v1/books/<id>___ xoa sach
@bp.delete("/<int:bid>")
def delete_book(bid):
    book = db.get_or_404(Book, bid)
    db.session.delete(book)
    db.session.commit()
    return "", 204


# ___GET /api/v1/books/<id>/authors___ tac gia cua sach (N:M, kem role)
@bp.get("/<int:bid>/authors")
def list_authors(bid):
    db.get_or_404(Book, bid)
    rows = db.session.execute(
        select(Author, BookAuthor.role)
        .join(BookAuthor, Author.id == BookAuthor.author_id)
        .where(BookAuthor.book_id == bid)
    ).all()
    return jsonify([{"id": a.id, "name": a.name, "role": r} for a, r in rows]), 200


# ___POST /api/v1/books/<id>/authors___ gan tac gia cho sach
@bp.post("/<int:bid>/authors")
def add_author(bid):
    db.get_or_404(Book, bid)
    req = request.get_json(silent=True) or {}
    if "author_id" not in req:
        abort(400, "Thieu author_id")
    db.get_or_404(Author, req["author_id"])
    p = BookAuthor(book_id=bid, author_id=req["author_id"], role=req.get("role", "co"))
    db.session.add(p)
    db.session.commit()
    return {"book_id": bid, "author_id": p.author_id, "role": p.role}, 201
