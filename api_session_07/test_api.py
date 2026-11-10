import pytest
from sqlalchemy import event
from config import TestConfig
from extensions import db
from factory import create_app


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def add_product(client, sku, qty=10):
    r = client.post("/api/v1/products", json={
        "sku": sku, "name": sku, "price_cents": 1000, "qty_in_stock": qty})
    return r.get_json()["id"]


# POST /api/v1/products: 201, trung sku thi 409
def test_create_product(client):
    body = {"sku": "IP-15", "name": "iPhone 15", "price_cents": 2000000}
    r = client.post("/api/v1/products", json=body)
    assert r.status_code == 201
    assert r.get_json()["sku"] == "IP-15"
    assert r.get_json()["qty_in_stock"] == 0

    r = client.post("/api/v1/products", json=body)
    assert r.status_code == 409


# POST /api/v1/orders: 201 va tru qty_in_stock
def test_create_order(client):
    pid = add_product(client, "IP-15", qty=5)
    r = client.post("/api/v1/orders", json={
        "items": [{"product_id": pid, "qty": 2}]})
    assert r.status_code == 201
    assert r.get_json()["items"][0]["qty"] == 2

    product = client.get(f"/api/v1/products/{pid}").get_json()
    assert product["qty_in_stock"] == 3


# GET /api/v1/orders co selectinload: 5 don van chi 2 query (khong bi N+1)
def test_list_orders_no_n_plus_1(app, client):
    p1 = add_product(client, "P-001")
    p2 = add_product(client, "P-002")
    for _ in range(5):
        client.post("/api/v1/orders", json={"items": [
            {"product_id": p1, "qty": 1}, {"product_id": p2, "qty": 1}]})

    queries = []

    def count(conn, cursor, statement, *args):
        queries.append(statement)

    with app.app_context():
        engine = db.engine
    event.listen(engine, "before_cursor_execute", count)
    r = client.get("/api/v1/orders")
    event.remove(engine, "before_cursor_execute", count)

    assert r.status_code == 200
    assert len(r.get_json()) == 5
    assert len(queries) == 2
