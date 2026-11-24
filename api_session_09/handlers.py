def v1_create_order(body):
    return {"account_id": body.get("account_id"), "status": "created"}


def v2_create_order(body):
    return {"order": {"account_id": body.get("account_id"), "state": "CREATED"}}
