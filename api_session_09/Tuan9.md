# Lab01

Chạy server:
![alt text](lab1_server.png)

Kết quả gọi v1 (trả `full_name`):
![alt text](lab1_v1.png)

Kết quả gọi v2 (tách `first_name`, `last_name`):
![alt text](lab1_v2.png)

# Lab02

Chạy server:
![alt text](lab2_server.png)

Không gửi header (mặc định v2):
![alt text](lab2_default.png)

`X-API-Version: 1` (trả `full_name`):
![alt text](lab2_v1.png)

`X-API-Version: 2024-06-20`:
![alt text](lab2_dated.png)

`X-API-Version: 99` (version lạ trả 400, không fallback):
![alt text](lab2_unsupported.png)

# Lab03

Thêm `sunset.py` có decorator `@deprecate_at(date)`, gắn vào route v1 trong `blueprints/v1.py` (sunset 31/12/2026). Trước ngày sunset trả 200 kèm header `Sunset`, `Deprecation: true`, `Link` tới v2; sau ngày sunset trả 410 Gone. Thêm route `/api/v0/users/{id}` có ngày sunset đã qua (01/01/2026) để test trường hợp 410.

Chạy server (mỗi lần gọi v1 log `deprecated_call`):
![alt text](lab3_server.png)

Gọi v1 trước sunset (200, có `Sunset`, `Deprecation`, `Link`):
![alt text](lab3_v1.png)

Gọi v0 sau sunset (410 Gone):
![alt text](lab3_v0_gone.png)
