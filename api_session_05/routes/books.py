import json
import os
from flask import Blueprint, abort, jsonify, request
from jsonschema import ValidationError, validate
from sqlalchemy import select
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


# ___GET /api/v1/books___ lay danh sach sach
@bp.get("")
def list_books():
    rows = db.session.scalars(select(Book).order_by(Book.id)).all()
    return jsonify([b.to_dict() for b in rows]), 200


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
