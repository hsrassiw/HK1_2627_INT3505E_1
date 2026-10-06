from app import app

client = app.test_client()
URL = "/api/v1/orders"


# di het cac trang bang next_cursor, tra ve tat ca don
def get_all(query):
    result = []
    cursor = None
    while True:
        url = f"{URL}?{query}"
        if cursor:
            url += f"&cursor={cursor}"
        body = client.get(url).get_json()
        result += body["data"]
        cursor = body["next_cursor"]
        if not cursor:
            return result


# ___Test cursor___
def test_limit():
    body = client.get(f"{URL}?limit=5").get_json()
    assert [o["id"] for o in body["data"]] == [1, 2, 3, 4, 5]
    assert body["next_cursor"] is not None


def test_cursor_next_page():
    cursor = client.get(f"{URL}?limit=5").get_json()["next_cursor"]
    body = client.get(f"{URL}?limit=5&cursor={cursor}").get_json()
    assert [o["id"] for o in body["data"]] == [6, 7, 8, 9, 10]


def test_cursor_get_all():
    ids = [o["id"] for o in get_all("limit=7")]
    assert ids == list(range(1, 26))


def test_last_page_no_cursor():
    body = client.get(f"{URL}?limit=100").get_json()
    assert len(body["data"]) == 25
    assert body["next_cursor"] is None


def test_bad_cursor():
    r = client.get(f"{URL}?cursor=hong")
    assert r.status_code == 400
    assert r.content_type == "application/problem+json"
    assert r.get_json()["title"] == "Invalid cursor"


def test_cursor_not_exist():
    # base64 cua {"id": 999}
    r = client.get(f"{URL}?cursor=eyJpZCI6IDk5OX0=")
    assert r.status_code == 400


# ___Test sort___
def test_sort_asc():
    totals = [o["total"] for o in get_all("sort=total&limit=4")]
    assert totals == sorted(totals)


def test_sort_desc():
    totals = [o["total"] for o in get_all("sort=-total&limit=4")]
    assert totals == sorted(totals, reverse=True)


def test_sort_with_cursor_no_duplicate():
    ids = [o["id"] for o in get_all("sort=-total&limit=4")]
    assert len(ids) == 25
    assert len(set(ids)) == 25


def test_bad_sort():
    r = client.get(f"{URL}?sort=price")
    assert r.status_code == 400
    assert r.content_type == "application/problem+json"
