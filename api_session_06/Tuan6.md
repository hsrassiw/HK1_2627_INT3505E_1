## Lab1

User mẫu (mật khẩu đều là `secret123`, lưu dạng hash bcrypt):

| Email | Role | Scope |
| --- | --- | --- |
| an@vnu.edu.vn | manager | orders:read, orders:write |
| binh@vnu.edu.vn | manager | orders:read, orders:write |
| chi@vnu.edu.vn | viewer | (không có) |

Endpoint:

| Endpoint | Method | Mô tả |
| --- | --- | --- |
| `/api/auth/login` | POST | đăng nhập, trả về access + refresh token |
| `/api/auth/refresh` | POST | dùng refresh token lấy access token mới |
| `/api/orders` | GET | cần access token và scope `orders:read` |

Chạy server:
![Chạy server](lab1_server.png)

Kết quả test đăng nhập sai mật khẩu (401 Unauthorized):
![Login 401](lab1_login_401.png)

Kết quả test đăng nhập đúng (200 OK, trả về access + refresh):
![Login 200](lab1_login_200.png)

Kết quả test gọi `/api/orders` không có token (401 Unauthorized):
![Không có token](lab1_no_token.png)

Kết quả test gọi `/api/orders` có token (200 OK):
![Có token](lab1_orders.png)

Kết quả test refresh lấy access token mới (200 OK):
![Refresh](lab1_refresh.png)
