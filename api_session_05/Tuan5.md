## Lab1

Entity và quan hệ:

| Entity | Fields chính | Quan hệ |
| --- | --- | --- |
| Book | title, isbn, price_vnd, stock | N:1 Category; N:M Author |
| Author | name, bio | N:M Book |
| Category | name, slug | 1:N Book |
| Review | rating, book_id, user_id | N:1 Book; N:1 User |
| User | email, display_name | 1:N Review |

Endpoint:

| Endpoint | Method |
| --- | --- |
| `/api/v1/books` | GET, POST |
| `/api/v1/books/{id}` | GET, PUT, DELETE |
| `/api/v1/books/{id}/authors` | GET, POST |

Chạy server:
![Chạy server](lab1_server.png)

Kết quả test GET danh sách sách (200 OK):
![GET 200](lab1_get_all.png)

Kết quả test POST tạo sách mới (201 Created):
![POST 201](lab1_post_201.png)

Kết quả test POST sai schema (400 Bad Request):
![POST 400](lab1_post_400.png)

Kết quả test xem tác giả của sách (200 OK):
![Tác giả](lab1_authors.png)
