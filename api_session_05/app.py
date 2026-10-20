import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from models import Author, Book, Category, Review, User, db
from routes.books import bp

app = Flask(__name__)
app.json.ensure_ascii = False
app.json.sort_keys = False
# test dat DATABASE_URL de dung DB rieng
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///bookstore.db")
db.init_app(app)
app.register_blueprint(bp)


@app.errorhandler(HTTPException)
def handle_http(e):
    return jsonify(error=e.name, message=e.description), e.code


# du lieu mau, chi them khi DB con trong
def seed():
    tech = Category(name="Cong nghe", slug="tech")
    novel = Category(name="Tieu thuyet", slug="novel")
    a1 = Author(name="Robert C. Martin", bio="Uncle Bob")
    a2 = Author(name="Martin Fowler", bio="Refactoring")
    a3 = Author(name="Nguyen Nhat Anh", bio="Nha van")
    db.session.add_all([tech, novel, a1, a2, a3])

    books = [
        Book(title="Clean Code", isbn="9780132350884", price_vnd=450000, stock=14, category=tech, authors=[a1]),
        Book(title="Clean Architecture", isbn="9780134494166", price_vnd=420000, stock=5, category=tech, authors=[a1]),
        Book(title="Refactoring", isbn="9780134757599", price_vnd=450000, stock=0, category=tech, authors=[a2]),
        Book(title="Patterns of Enterprise", isbn="9780321127426", price_vnd=520000, stock=3, category=tech, authors=[a2]),
        Book(title="Mat biec", isbn="9786041000001", price_vnd=110000, stock=20, category=novel, authors=[a3]),
        Book(title="Cho toi xin mot ve di tuoi tho", isbn="9786041000002", price_vnd=85000, stock=8, category=novel, authors=[a3]),
        Book(title="Toi thay hoa vang tren co xanh", isbn="9786041000003", price_vnd=110000, stock=12, category=novel, authors=[a3]),
        Book(title="Kinh van hoa", isbn="9786041000004", price_vnd=150000, stock=0, category=novel, authors=[a3]),
    ]
    db.session.add_all(books)

    u1 = User(email="an@example.com", display_name="An")
    u2 = User(email="binh@example.com", display_name="Binh")
    db.session.add_all([u1, u2])
    db.session.flush()
    db.session.add_all([
        Review(rating=5, book_id=books[0].id, user_id=u1.id),
        Review(rating=4, book_id=books[0].id, user_id=u2.id),
        Review(rating=5, book_id=books[4].id, user_id=u1.id),
    ])
    db.session.commit()


with app.app_context():
    db.create_all()
    if db.session.scalar(db.select(Book).limit(1)) is None:
        seed()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
