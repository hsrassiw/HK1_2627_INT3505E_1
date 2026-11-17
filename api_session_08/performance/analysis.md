# Lab 4 — Phân tích kết quả

| Kịch bản | Users | Spawn rate | Duration | p95 (ms) | Failure rate | RPS |
|---|---:|---:|---:|---:|---:|---:|
| A | 10 | 2 | 30s | 11 | 0% (0/150) | 5.09 |
| B | 50 | 5 | 60s | 15 | 0.14% (2/1393) | 23.41 |
| C | 200 | 50 | 30s | 120 | 0.07% (2/2886) | 98.23 |

**1. Kịch bản có p95 cao nhất?**
C (120 ms). Từ A lên B p95 gần như không đổi (11 → 15 ms), nhưng lên 200 user thì tăng gấp 8 lần do Flask dev server và SQLite phải xếp hàng xử lý request. `POST /books` chậm nhất (p95 160 ms) vì ghi SQLite phải khoá file.

**2. Endpoint nào tăng failure rate?**
Chỉ `GET /books?year=` có lỗi (2 ở B, 2 ở C), đều là lỗi giả lập 1% do Locust tự gọi `response.failure()`, server không trả HTTP 500 thật. Tỉ lệ lỗi không tăng theo số user. 404 của `GET /books/{id}` là hành vi đúng nên tính là success.

**3. SLO p95 < 300 ms?**
Cả 3 kịch bản đều đạt, nhưng C có p99 = 210 ms, max = 330 ms đã sát ngưỡng. Đề xuất CI gate theo kịch bản B: p95 < 300 ms, lỗi thật < 1%. Giới hạn: dev server + SQLite, Locust chạy chung máy với server, mỗi kịch bản chạy 1 lần nên không khẳng định được SLO production.

**4. Connection pool giới hạn 5?**
Chỉ 5 request được dùng DB cùng lúc, còn lại phải chờ, quá `pool_timeout` thì trả 500. Kiểm chứng: đặt `SQLALCHEMY_ENGINE_OPTIONS = {"pool_size": 5, "max_overflow": 0, "pool_timeout": 2}`, chạy lại kịch bản C rồi so p95/p99 và xem bảng Failures có lỗi 500 thật không.
