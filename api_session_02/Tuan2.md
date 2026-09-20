## Bài 1

Chạy server:
![Chạy server](bai1_server.png)

Kết quả test tạo mới thành công (201 Created):
![201](bai1_post_success.png)

Kết quả test lỗi thiếu field (422 Unprocessable Entity):
![ 422](bai1_error_422.png)

Kết quả test lỗi thiếu Content-Type (415 Unsupported Media Type):
![415](bai1_error_415.png)

Kết quả test lỗi sai cú pháp JSON (400 Bad Request):
![L400](bai1_error_400.png)

## Bài 2

Kết quả test GET chi tiết theo ID (200 OK):
![GET 200](bai2_get_detail.png)

Kết quả test PATCH cập nhật một phần (200 OK):
![PATCH 200](bai2_patch_success.png)

Kiểm tra lại sau khi PATCH:
![Kiểm tra sau PATCH](bai2_check_after_patch.png)

Kết quả test PUT (200 OK):
![PUT 200](bai2_put_success.png)

Kết quả test DELETE xoá sách (204 No Content):
![DELETE 204](bai2_delete_success.png)

Kết quả test GET không tìm thấy sau khi xoá (404 Not Found):
![GET 404](bai2_get_not_found.png)

## Bài 3

Kết quả test phân trang trang 1 (page=1&size=2):
![Phân trang trang 1](bai3_page1.png)

Kết quả test phân trang trang 2 có link prev và next (page=2&size=2):
![Phân trang trang 2](bai3_page2.png)

Kết quả test lọc theo tác giả (author=Orwell):
![Lọc theo tác giả](bai3_filter_author.png)

Kết quả test tìm kiếm từ khoá trong tiêu đề (q=clean):
![Tìm kiếm từ khoá](bai3_search_query.png)

Kết quả test lỗi tham số không phải số nguyên (400 Bad Request):
![Lỗi tham số 400](bai3_error_page_int.png)

Kết quả test Header Accept application/json (200 OK):
![Header Accept](bai3_accept_header.png)