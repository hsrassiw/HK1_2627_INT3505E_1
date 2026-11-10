from marshmallow import Schema, fields, validate


# ___ output ___
class ProductOut(Schema):
    id = fields.Int()
    sku = fields.Str()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    price_cents = fields.Int()
    qty_in_stock = fields.Int()
    archived = fields.Bool()


# ___ input tao moi ___
class ProductIn(Schema):
    sku = fields.Str(required=True,
                     validate=validate.Length(min=3, max=32))
    name = fields.Str(required=True,
                      validate=validate.Length(min=1, max=255))
    price_cents = fields.Int(required=True,
                             validate=validate.Range(min=0))
    qty_in_stock = fields.Int(load_default=0,
                              validate=validate.Range(min=0))


# ___ PATCH: chi field co trong body moi doi ___
class ProductPatch(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=255))
    price_cents = fields.Int(validate=validate.Range(min=0))


# ___ /reserve ___
class ReserveIn(Schema):
    qty = fields.Int(required=True, validate=validate.Range(min=1))


# ___ order ___
class OrderItemIn(Schema):
    product_id = fields.Int(required=True)
    qty = fields.Int(required=True, validate=validate.Range(min=1))


class OrderIn(Schema):
    items = fields.List(fields.Nested(OrderItemIn), required=True,
                        validate=validate.Length(min=1))


class OrderItemOut(Schema):
    product_id = fields.Int()
    qty = fields.Int()
    unit_price_cents = fields.Int()


class OrderOut(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    items = fields.List(fields.Nested(OrderItemOut))
