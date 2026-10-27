# Security Audit

Rà soát 3 endpoint trong [openapi.yaml](openapi.yaml): `POST /auth/login`, `POST /auth/refresh`, `GET /posts/{id}`.

| # | Điểm có thể lộ | Endpoint | Rủi ro | Cách chặn |
| --- | --- | --- | --- | --- |
| 1 | Dò mật khẩu | `POST /auth/login` | Thử liên tục nhiều mật khẩu (brute-force) hoặc dùng email/mật khẩu bị lộ từ trang khác | Rate-limit theo IP và theo email, quá giới hạn trả 429 |
| 2 | Lộ email đã đăng ký | `POST /auth/login` | Sai email và sai mật khẩu trả lỗi khác nhau, hoặc email không tồn tại thì trả nhanh hơn (không chạy bcrypt) | Luôn trả chung 401 `invalid_credentials`; email không tồn tại vẫn chạy bcrypt với hash giả |
| 3 | Refresh token bị đánh cắp | `POST /auth/refresh` | Refresh sống 30 ngày, lộ ra là kẻ gian lấy access mới liên tục | Mỗi lần refresh cấp refresh mới và thu hồi cái cũ; có logout để thu hồi; chỉ nhận refresh token, gửi access token thì trả 401 |
| 4 | Xem bài của người khác bằng cách đổi id (BOLA) | `GET /posts/{id}` | Có scope `posts:read` nhưng đổi id là đọc được bài `private`, `friends` của người khác | Ngoài scope còn kiểm tra `visibility` và tác giả; không được xem thì trả 404 như bài không tồn tại để không lộ bài có tồn tại |
| 5 | JWT ký yếu hoặc token bị lộ khi truyền | cả 3 endpoint | Secret ngắn hoặc commit lên Git thì token giả được; chạy HTTP thì nghe lén được mật khẩu và token | Chỉ cho phép HS256, secret ngẫu nhiên ≥ 256 bit lấy từ biến môi trường, luôn kiểm `exp`; chỉ dùng HTTPS, không log mật khẩu và token |

Đã thể hiện trong spec:

- Login trả chung lỗi 401 và có 429 (điểm 1, 2).
- Refresh chỉ nhận refresh token, mỗi lần refresh cấp refresh mới (điểm 3).
- `GET /posts/{id}` cần scope `posts:read`, không được xem thì trả 404 (điểm 4).
