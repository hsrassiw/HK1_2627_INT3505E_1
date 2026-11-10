from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from errors import Conflict, NotFound, OutOfStock
from extensions import db
from models import Product
from schemas import ProductIn, ProductOut, ProductPatch, ReserveIn

products_bp = Blueprint("products", __name__, url_prefix="/api/v1/products")


# lay san pham con hoat dong (chua xoa), khong co thi 404
def get_active(id):
    p = db.session.get(Product, id)
    if p is None or p.archived:
        raise NotFound(message=f"product {id} not found")
    return p


# ___GET /api/v1/products?page=1&size=20___
@products_bp.get("")
def list_products():
    page = max(1, request.args.get("page", 1, type=int))
    size = min(100, max(1, request.args.get("size", 20, type=int)))
    base = db.select(Product).where(Product.archived.is_(False))
    rows = db.session.execute(
        base.order_by(Product.id).offset((page - 1) * size).limit(size)
    ).scalars().all()
    total = db.session.scalar(
        db.select(db.func.count()).select_from(Product)
        .where(Product.archived.is_(False)))
    return jsonify({
        "items": [ProductOut().dump(p) for p in rows],
        "page": page, "size": size, "total": total,
    }), 200


# ___GET /api/v1/products/<id>___
@products_bp.get("/<int:id>")
def get_product(id):
    return ProductOut().dump(get_active(id)), 200


# ___POST /api/v1/products___ 409 neu sku trung
@products_bp.post("")
def create_product():
    body = ProductIn().load(request.json)
    p = Product(**body)
    db.session.add(p)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Conflict(message="sku already exists")
    return ProductOut().dump(p), 201


# ___POST /api/v1/products/<id>/reserve___ 409 neu het hang
@products_bp.post("/<int:id>/reserve")
def reserve_product(id):
    body = ReserveIn().load(request.json)
    p = get_active(id)
    if p.qty_in_stock < body["qty"]:
        raise OutOfStock(message=f"only {p.qty_in_stock} left")
    p.qty_in_stock -= body["qty"]
    db.session.commit()
    return ProductOut().dump(p), 200


# ___PATCH /api/v1/products/<id>___
@products_bp.patch("/<int:id>")
def patch_product(id):
    body = ProductPatch().load(request.json, partial=True)
    p = get_active(id)
    for k, v in body.items():
        setattr(p, k, v)
    db.session.commit()
    return ProductOut().dump(p), 200


# ___DELETE /api/v1/products/<id>___ soft-delete
@products_bp.delete("/<int:id>")
def delete_product(id):
    p = get_active(id)
    p.archived = True
    db.session.commit()
    return "", 204
