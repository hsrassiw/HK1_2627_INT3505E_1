from flask import Blueprint, jsonify, request
from sqlalchemy.orm import selectinload
from errors import NotFound, OutOfStock
from extensions import db
from models import Order, OrderItem
from products import get_active
from schemas import OrderIn, OrderOut

orders_bp = Blueprint("orders", __name__, url_prefix="/api/v1/orders")


# eager load items (1-N) bang selectinload, tranh N+1
def select_orders():
    return db.select(Order).options(selectinload(Order.items))


# ___GET /api/v1/orders___
@orders_bp.get("")
def list_orders():
    rows = db.session.execute(
        select_orders().order_by(Order.id)).scalars().all()
    return jsonify([OrderOut().dump(o) for o in rows]), 200


# ___GET /api/v1/orders/<id>___
@orders_bp.get("/<int:id>")
def get_order(id):
    o = db.session.execute(
        select_orders().where(Order.id == id)).scalar()
    if o is None:
        raise NotFound(message=f"order {id} not found")
    return OrderOut().dump(o), 200


# ___POST /api/v1/orders___ body: {"items": [{"product_id": 1, "qty": 2}]}
@orders_bp.post("")
def create_order():
    body = OrderIn().load(request.json)
    order = Order()
    for it in body["items"]:
        p = get_active(it["product_id"])
        if p.qty_in_stock < it["qty"]:
            db.session.rollback()
            raise OutOfStock(message=f"{p.sku}: only {p.qty_in_stock} left")
        p.qty_in_stock -= it["qty"]
        order.items.append(OrderItem(
            product=p, qty=it["qty"], unit_price_cents=p.price_cents))
    db.session.add(order)
    db.session.commit()
    return OrderOut().dump(order), 201
