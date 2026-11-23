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
