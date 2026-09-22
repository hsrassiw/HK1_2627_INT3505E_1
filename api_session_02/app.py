# Bai 3

import sqlite3
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)
DEFAULT_SIZE, MAX_SIZE = 20, 100
DB_NAME = "database.db"

#Lay du lieu
def get_db():
    db = sqlite3.connect(DB_NAME)
    db.row_factory = (
        sqlite3.Row
    )
    return db

def init_db():
  db = get_db()
  db.execute(
      "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title, author,"
      " isbn, price)"
  )
  db.execute(
      "CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, book_id,"
      " quantity, total_price)"
  )
  db.commit()
  db.close()

#____GET /books____ tra danh sach
@app.get("/books")
def list_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify(error = "page and size must be int"), 400
    page = max(page, 1)
    size = max(min(size, MAX_SIZE), 1)

    db = get_db()
    sql = "SELECT * FROM books WHERE 1=1"
    args = []
    a = request.args.get("author")
    if a:
      sql += " AND lower(author) = lower(?)"
      args.append(a)
    q = request.args.get("q")
    if q:
      sql += " AND lower(title) LIKE lower(?)"
      args.append(f"%{q}%")
    total = len(db.execute(sql, args).fetchall())
    start = (page - 1) * size
    sql += " LIMIT ? OFFSET ?"
    rows = db.execute(sql, args + [size, start]).fetchall()
    items = [dict(r) for r in rows]
    db.close()
    last = (total + size - 1) // size if size else 1
    def u(p):
      return f"/books?page={p}&size={size}"
    links = {
        "self": {"href": u(page)},
        "first": {"href": u(1)},
        "last": {"href": u(max(last, 1))},
    }
    if page > 1:
      links["prev"] = {"href": u(page - 1)}
    if start + size < total:
      links["next"] = {"href": u(page + 1)}
    body = {
        "data": items,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": last,
        },
        "_links": links,
    }
    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"] = "public, max-age=30"
    return resp


# ____GET /books/<id>____ xem chi tiet
@app.get("/books/<int:bid>")
def fetch(bid):
    db = get_db()
    row = db.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
    db.close()
    if not row:
        return jsonify(error="not found"), 404
    resp = make_response(jsonify(dict(row)), 200)
    resp.headers["Cache-Control"] = "max-age=60"
    return resp

#___POST /books___ tao moi
@app.post("/books")
def create_book():
  if not request.is_json:
    return jsonify(error="expected JSON"), 415
  p = request.get_json(silent=True)
  if p is None:
    return jsonify(error="invalid JSON"), 400
  t = (p.get("title") or "").strip()
  a = (p.get("author") or "").strip()
  if not t or not a:
    return jsonify(error="title and author required"), 422
  db = get_db()
  cur = db.execute(
      "INSERT INTO books (title, author, isbn, price) VALUES (?, ?, ?, ?)",
      (t, a, p.get("isbn"), p.get("price")),
  )
  db.commit()
  book = dict(
      db.execute("SELECT * FROM books WHERE id = ?", (cur.lastrowid,)).fetchone()
  )
  db.close()
  resp = make_response(jsonify(book), 201)
  resp.headers["Location"] = f"/books/{book['id']}"
  return resp

#___PUT __thay toan bo
@app.put("/books/<int:bid>")
def put(bid):
  db = get_db()
  row = db.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
  if not row:
    db.close()
    return jsonify(error="not found"), 404
  p = request.get_json(silent=True) or {}
  t, a = p.get("title"), p.get("author")
  if not t or not a:
    db.close()
    return jsonify(error="need title+author"), 422
  db.execute(
      "UPDATE books SET title = ?, author = ?, isbn = ?, price = ? WHERE id ="
      " ?",
      (t.strip(), a.strip(), p.get("isbn"), p.get("price"), bid),
  )
  db.commit()
  book = dict(
      db.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
  )
  db.close()
  return jsonify(book), 200

#__PATCH__ chi cap nhat mot phan
@app.patch("/books/<int:bid>")
def patch(bid):
  db = get_db()
  row = db.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
  if not row:
    db.close()
    return jsonify(error="not found"), 404
  p = request.get_json(silent=True) or {}
  if p.get("price", 0) < 0:
    db.close()
    return jsonify(error="price must be positive"), 422
  for k in "title author isbn price".split():
    if k in p:
      db.execute(f"UPDATE books SET {k} = ? WHERE id = ?", (p[k], bid))
  db.commit()
  book = dict(
      db.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
  )
  db.close()
  return jsonify(book), 200


#___DELETE___Xoa
@app.delete("/books/<int:bid>")
def delete(bid):
  db = get_db()
  row = db.execute("SELECT * FROM books WHERE id = ?", (bid,)).fetchone()
  if not row:
    db.close()
    return jsonify(error="not found"), 404
  db.execute("DELETE FROM books WHERE id = ?", (bid,))
  db.commit()
  db.close()
  return "", 204

# ___GET /orders/<oid>___ xem don hang
@app.get("/orders/<int:oid>")
def get_order(oid):
  db = get_db()
  row = db.execute("SELECT * FROM orders WHERE id = ?", (oid,)).fetchone()
  db.close()
  if not row:
    return jsonify(error="not found"), 404
  return jsonify(dict(row)), 200

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)

