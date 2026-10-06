## Lab1

Bảng endpoint:

| Endpoint | Method | Dạng |
| --- | --- | --- |
| `/api/v1/users` | GET, POST | Collection |
| `/api/v1/users/{id}` | GET, PATCH | Item |
| `/api/v1/posts` | GET, POST | Collection |
| `/api/v1/posts/{id}` | GET, PUT, PATCH, DELETE | Item |
| `/api/v1/comments` | GET, POST | Collection |
| `/api/v1/comments/{id}` | GET, PATCH, DELETE | Item |
| `/api/v1/tags` | GET, POST | Collection |
| `/api/v1/follows` | GET, POST | Collection |
| `/api/v1/follows/{id}` | DELETE | Item |

Sơ đồ cây endpoint:
![Sơ đồ cây endpoint](<Sơ đồ cây endpoint.png>)

Chú thích: nét liền là cấp path (/), nét đứt là query parameter dùng để lọc (?)

Chạy server:
![Chạy server](lab1_server.png)

Kết quả test GET danh sách bài viết (200 OK):
![GET 200](lab1_get_all.png)

Kết quả test lọc theo user (user_id=1):
![Lọc theo user](lab1_get_user_id.png)

Kết quả test lọc theo tag (tag=api):
![Lọc theo tag](lab1_get_tag.png)

Kết quả test POST tạo mới thành công (201 Created):
![POST 201](lab1_post_success.png)

## Lab2

Chạy server:
![Chạy server](lab2_server.png)

Kết quả test GET bài viết không tồn tại (404 Not Found):
![404](lab2_404_post.png)

Kết quả test URL không tồn tại (404 Not Found):
![404 URL](lab2_404_url.png)

Kết quả test sai method (405 Method Not Allowed):
![405](lab2_405.png)

Kết quả test lỗi sai cú pháp JSON (400 Bad Request):
![400](lab2_400.png)

Kết quả test lỗi thiếu field (422 Unprocessable Entity):
![422](lab2_422.png)

Kết quả test lỗi server (500 Internal Server Error):
![500](lab2_500.png)
![server](lab2_500log.png)