## Bài 1

Chạy server:
![Chạy server](bai1_server.png)

Kết quả test:
![Gọi API](bai1_curl.png)

## Bài 2

Chạy server:
![Chạy server](bai2_server.png)

Kết quả test GET /health:
![Kết quả test health](bai2_health.png)

Kết quả test POST /echo:
![Kết quả test echo](bai2_echo.png)

## Bài 3

Chạy server:
![Chạy server](bai3_server.png)

Kết quả test thành công (201 Created):
![Test thành công](bai3_success.png)

Kết quả test lỗi thiếu dữ liệu (400 Bad Request):
![Test lỗi 400](bai3_error.png)

## Bài 4

Chạy server:
![Chạy server](bai4_server.png)

Kết quả test Path param thành công (200 OK):
![Path param 200](bai4_path_success.png)

Kết quả test Path param không tìm thấy (404 Not Found):
![Path param 404](bai4_path_not_found.png)

Kết quả test Query string giới hạn số lượng (limit=2):
![Query string limit](bai4_limit.png)

Kết quả test Query string tìm kiếm theo tên (q=van):
![Query string search](bai4_query.png)

## Bài 5

Chạy server:
![Chạy server](bai5_server.png)

Kết quả test xung đột quy tắc (409 Conflict):
![Xoá thất bại 409](bai5_delete_conflict.png)

Kết quả test xoá thành công (204 No Content):
![Xoá thành công 204](bai5_delete_success.png)

Kết quả test không tìm thấy sinh viên (404 Not Found):
![Xoá lỗi 404](bai5_delete_not_found.png)

Kiểm tra lại danh sách sau khi xoá:
![Kiểm tra danh sách](bai5_check_list.png)

## Bài 6

Kết quả test GET danh sách (200 OK):
![GET danh sách](bai6_get_list.png)

Kết quả test GET chi tiết theo ID (200 OK):
![GET chi tiết 200](bai6_get_detail.png)

Kết quả test GET không tìm thấy (404 Not Found):
![GET lỗi 404](bai6_get_not_found.png)

Kết quả test POST tạo mới sinh viên (201 Created):
![POST tạo mới 201](bai6_post_success.png)

Kết quả test PUT cập nhật sinh viên (200 OK):
![PUT cập nhật 200](bai6_put_success.png)

Kết quả test DELETE xoá sinh viên (204 No Content):
![DELETE xoá 204](bai6_delete_success.png)

Kết quả test POST lỗi thiếu dữ liệu (400 Bad Request):
![POST lỗi 400](bai6_post_error.png)

Kiểm tra lại danh sách cuối cùng:
![Kiểm tra danh sách cuối](bai6_check_final.png)

### Bài 6++

Kết quả test tìm kiếm theo tên (q=van):
![Tìm kiếm theo tên](bai6++_search.png)

Kết quả test sắp xếp theo tên (sort=name):
![Sắp xếp theo tên](bai6++_sort.png)

Kết quả test tạo mới với year hợp lệ >= 1900 (201 Created):
![Tạo mới year hợp lệ](bai6++_year_success.png)

Kết quả test lỗi year < 1900 (400 Bad Request):
![Lỗi year](bai6++_year_error.png)

Kết quả test kết hợp tìm kiếm và sắp xếp:
![Tìm kiếm và sắp xếp](bai6++_search_sort.png)