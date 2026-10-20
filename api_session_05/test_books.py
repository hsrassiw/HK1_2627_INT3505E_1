import os

# dung DB trong RAM, khong dung vao bookstore.db
os.environ["DATABASE_URL"] = "sqlite://"

from app import app

client = app.test_client()
URL = "/api/v1/books"


def ids(body):
    return [b["id"] for b in body["data"]]


# di het cac trang bang page.next, tra ve tat ca id
def get_all(query):
    result = []
    cursor = None
    while True:
        url = f"{URL}?{query}"
        if cursor:
            url += f"&cursor={cursor}"
        body = client.get(url).get_json()
        result += ids(body)
        cursor = body["page"]["next"]
        if not cursor:
            return result


# ___Test strategy___
def test_default_is_cursor():
    body = client.get(f"{URL}?limit=3").get_json()
    assert ids(body) == ["book_8", "book_7", "book_6"]
    assert body["page"]["more"] is True


def test_cursor_get_all():
    all_ids = get_all("limit=3")
    assert all_ids == [f"book_{i}" for i in range(8, 0, -1)]


def test_offset_first_page():
    body = client.get(f"{URL}?strategy=offset&limit=3").get_json()
    assert ids(body) == ["book_8", "book_7", "book_6"]
    assert body["pagination"] == {"offset": 0, "limit": 3, "total": 8, "has_next": True}


def test_offset_last_page():
    body = client.get(f"{URL}?strategy=offset&limit=3&offset=6").get_json()
    assert ids(body) == ["book_2", "book_1"]
    assert body["pagination"]["has_next"] is False


def test_bad_strategy():
    r = client.get(f"{URL}?strategy=page")
    assert r.status_code == 400
    assert r.get_json()["error"] == "bad_strategy"


# ___Test genre___
def test_genre():
    body = client.get(f"{URL}?genre=novel").get_json()
    assert len(body["data"]) == 4
    assert all(b["category"]["slug"] == "novel" for b in body["data"])


def test_genre_offset_total():
    body = client.get(f"{URL}?strategy=offset&genre=tech").get_json()
    assert body["pagination"]["total"] == 4


def test_genre_not_exist():
    body = client.get(f"{URL}?genre=abc").get_json()
    assert body["data"] == []


# ___Test sort multi-key___
# gia: 4=520k, 1=450k (Clean Code), 3=450k (Refactoring), 2=420k,
#      8=150k, 5=110k (Mat biec), 7=110k (Toi thay...), 6=85k
def test_sort_multi():
    body = client.get(f"{URL}?strategy=offset&sort=-price,title").get_json()
    assert ids(body) == [f"book_{i}" for i in [4, 1, 3, 2, 8, 5, 7, 6]]


def test_sort_multi_mixed():
    body = client.get(f"{URL}?strategy=offset&sort=price,-title").get_json()
    assert ids(body) == [f"book_{i}" for i in [6, 7, 5, 8, 2, 3, 1, 4]]


def test_cursor_same_as_offset():
    offset_ids = ids(client.get(f"{URL}?strategy=offset&sort=-price,title").get_json())
    assert get_all("sort=-price,title&limit=3") == offset_ids


def test_bad_sort():
    r = client.get(f"{URL}?sort=-price,foo")
    assert r.status_code == 400
    assert r.get_json()["error"] == "bad_sort"


def test_sort_changed():
    cursor = client.get(f"{URL}?limit=3").get_json()["page"]["next"]
    r = client.get(f"{URL}?sort=price&cursor={cursor}")
    assert r.status_code == 400
    assert r.get_json()["error"] == "sort_changed"
