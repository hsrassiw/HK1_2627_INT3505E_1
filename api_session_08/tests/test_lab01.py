"""LAB 1 — add your five tests here. Do not delete the smoke tests.

A. GET /books, empty database -> HTTP 200 and []
B. GET /books/9999 -> HTTP 404, JSON code == NOT_FOUND
C. POST /books with only author -> HTTP 400, errors contains title
D. POST valid book, DELETE it, GET same id -> HTTP 404
BONUS. Validate a Book response using JSON Schema; add an unknown
       field to a *copy* of the response and assert ValidationError.

Useful imports:
    from jsonschema import validate, ValidationError
    import pytest
    from tools import get_book_schema

Do not depend on test execution order. Fixtures: client, app, sample_book.
"""

import pytest
from jsonschema import ValidationError, validate
from tools import get_book_schema

# A. GET /books khi CSDL rỗng -> 200 và mảng rỗng []
def test_get_books_empty_returns_empty_list(client):
    r = client.get("/books")
    assert r.status_code == 200
    data = r.get_json()
    assert data is not None
    assert data == []

# B. GET /books/<id> không tồn tại -> 404, code == "NOT_FOUND"
def test_get_nonexistent_book_returns_404(client):
    r = client.get("/books/9999")
    assert r.status_code == 404
    body = r.get_json()
    assert body["code"] == "NOT_FOUND"

# C. POST /books thiếu title -> 400 và trong errors có field "title"
def test_post_book_missing_title_returns_400(client):
    r = client.post("/books", json={"author": "J.J. Geewax"})
    assert r.status_code == 400
    body = r.get_json()
    error_fields = {err["field"] for err in body.get("errors", [])}
    assert "title" in error_fields

# D. Xoá rồi GET cùng id -> 404
def test_delete_then_get_same_id_returns_404(client, sample_book):
    del_res = client.delete(f"/books/{sample_book}")
    assert del_res.status_code == 204
    get_res = client.get(f"/books/{sample_book}")
    assert get_res.status_code == 404

def test_response_extra_field_blocked(client, sample_book):
    schema = get_book_schema()
    schema["properties"]["year"]["type"] = ["integer", "null"]
    schema["properties"]["isbn"]["type"] = ["string", "null"]

    body = client.get(f"/books/{sample_book}").get_json()
    body["password_hash"] = "secret"
    with pytest.raises(ValidationError):
        validate(body, schema)