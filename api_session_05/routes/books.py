import base64
import json
import os
from flask import Blueprint, abort, jsonify, request
from jsonschema import ValidationError, validate
from sqlalchemy import and_, func, or_, select
from models import Author, Book, BookAuthor, Category, db

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


# ___BTVN 2___ offset + cursor, filter genre, sort nhieu cot
# chi cho sort theo cac cot trong whitelist
SORT = {"id": Book.id, "price": Book.price_vnd, "title": Book.title}


def bad(err, msg):
    return jsonify(error=err, message=msg), 400


# "-price,title" -> [(Book.price_vnd, True), (Book.title, False), (Book.id, False)]
def parse_sort(raw):
    keys = []
    for s in raw.split(","):
        desc = s.startswith("-")
        name = s.lstrip("-")
        if name not in SORT:
            return None
        keys.append((SORT[name], desc))
    # luon sort them theo id de 2 sach trung gia tri van co thu tu co dinh
    keys.append((Book.id, keys[-1][1]))
    return keys


def _enc(s):
    return base64.urlsafe_b64encode(json.dumps(s).encode()).decode().rstrip("=")


def _dec(raw):
    pad = "=" * (-len(raw) % 4)
    return json.loads(base64.urlsafe_b64decode(raw + pad))


# lay cac sach nam sau sach cuoi cua trang truoc
# vd sort=-price: price < v0 HOAC (price = v0 VA id < v1)
def after(keys, values):
    conds = []
    for n, (col, desc) in enumerate(keys):
        same = [keys[j][0] == values[j] for j in range(n)]
        nxt = col < values[n] if desc else col > values[n]
        conds.append(and_(*same, nxt))
    return or_(*conds)


# cursor = {"s": sort, "v": [gia tri cac cot sort cua sach cuoi]}
def apply_cursor(q, raw, sort, keys):
    if not raw:
        return q, None
    try:
        c = _dec(raw)
        s, values = c["s"], list(c["v"])
    except Exception:
        return None, "bad_cursor"
    if s != sort or len(values) != len(keys):
        return None, "sort_changed"
    return q.where(after(keys, values)), None


def build_response(items, sort, keys, more):
    nxt = None
    if items and more:
        last = items[-1]
        nxt = _enc({"s": sort, "v": [getattr(last, col.key) for col, _ in keys]})
    return jsonify(data=[b.to_dict() for b in items], page={"next": nxt, "more": more}), 200


# ___GET /api/v1/books___ lay danh sach sach
@bp.get("")
def list_books():
    a = request.args
    strategy = a.get("strategy", "cursor")
    if strategy not in ("cursor", "offset"):
        return bad("bad_strategy", "strategy chi nhan cursor hoac offset")
    lim = max(1, min(a.get("limit", 20, type=int), 100))
    sort = a.get("sort", "-id")
    keys = parse_sort(sort)
    if keys is None:
        return bad("bad_sort", f"khong sort duoc theo {sort}")

    conds = []
    if a.get("category", type=int):
        conds.append(Book.category_id == a.get("category", type=int))
    if a.get("genre"):
        conds.append(Book.category.has(Category.slug == a["genre"]))
    q = select(Book).where(*conds).order_by(*[c.desc() if d else c.asc() for c, d in keys])

    # offset: nhay trang duoc, co total
    if strategy == "offset":
        o = max(0, a.get("offset", 0, type=int))
        total = db.session.scalar(select(func.count(Book.id)).where(*conds))
        rows = db.session.scalars(q.offset(o).limit(lim)).all()
        return jsonify(
            data=[b.to_dict() for b in rows],
            pagination={"offset": o, "limit": lim, "total": total, "has_next": o + lim < total},
        ), 200

    # cursor: lay du 1 dong de biet con trang sau khong
    q, err = apply_cursor(q, a.get("cursor"), sort, keys)
    if err:
        return bad(err, "cursor khong hop le")
    rows = db.session.scalars(q.limit(lim + 1)).all()
    return build_response(rows[:lim], sort, keys, len(rows) > lim)


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
