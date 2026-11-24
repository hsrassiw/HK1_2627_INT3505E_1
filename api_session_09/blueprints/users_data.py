USERS = {
    1: {
        "id": 1,
        "first_name": "An",
        "last_name": "Nguyen",
        "email": "an.nguyen@example.com",
    },
    2: {
        "id": 2,
        "first_name": "Binh",
        "last_name": "Tran",
        "email": "binh.tran@example.com",
    },
}


def get_user(uid):
    """Return a user dict by id, or None if not found."""
    return USERS.get(uid)


def create_user(first_name, last_name, email):
    uid = max(USERS) + 1
    USERS[uid] = {"id": uid, "first_name": first_name,
                  "last_name": last_name, "email": email}
    return USERS[uid]
