## 1. API được chọn

Chọn GitHub REST API, base URL `https://api.github.com`. Năm endpoint đều thuộc nhóm Issues. Endpoint `GET` có thể đọc dữ liệu công khai mà không cần token; các endpoint ghi cần token có quyền `Issues: write`. Các request dùng những header sau:

```http
Accept: application/vnd.github+json
Authorization: Bearer <TOKEN>
X-GitHub-Api-Version: 2026-03-10
Content-Type: application/json
```

`Authorization` chỉ cần cho các thao tác ghi; `Content-Type` dùng khi request có JSON body. Response có body thường trả `Content-Type`; các response còn có nhóm `X-RateLimit-*`. Riêng `GET` hỗ trợ cache qua `Cache-Control`, `ETag` và `Last-Modified`.

## 2. Audit năm endpoint

| Endpoint | Method | Status code chính | Response headers chính | Đánh giá theo REST |
|---|:---:|---|---|---|
| `/repos/{owner}/{repo}/issues/{issue_number}` — đọc một issue | `GET` | `200`, `301`, `304`, `404`, `410` | `Content-Type`, `Cache-Control`, `ETag`, `Last-Modified`, `X-RateLimit-*` | **Resource-oriented, Level 2.** `GET` chỉ đọc nên an toàn và idempotent. |
| `/repos/{owner}/{repo}/issues` — tạo issue | `POST` | `201`, `400`, `403`, `404`, `410`, `422`, `503` | `Content-Type`, `X-RateLimit-*` | **Resource-oriented, Level 2.** `POST` tạo phần tử mới trong tập `/issues` và không idempotent mặc định. |
| `/repos/{owner}/{repo}/issues/{issue_number}` — cập nhật issue | `PATCH` | `200`, `301`, `403`, `404`, `410`, `422`, `503` | `Content-Type`, `X-RateLimit-*` | **Resource-oriented, Level 2.** `PATCH` phù hợp với cập nhật một phần representation. |
| `/repos/{owner}/{repo}/issues/{issue_number}/lock` — khóa issue | `PUT` | `204`, `403`, `404`, `410`, `422` | `X-RateLimit-*`; không có response body khi `204` | **Resource-oriented, Level 2.** `lock` được mô hình thành tài nguyên con; gọi lặp lại không tạo thêm trạng thái mới. |
| `/repos/{owner}/{repo}/issues/{issue_number}/lock` — mở khóa issue | `DELETE` | `204`, `403`, `404` | `X-RateLimit-*`; không có response body khi `204` | **Resource-oriented, Level 2.** `DELETE` xóa tài nguyên khóa và có tính idempotent. |

## 3. Về tính RESTful

Các URI đều dùng danh từ và có phân cấp tài nguyên rõ ràng; không sử dụng URL kiểu `/createIssue` hay `/unlockIssue`. HTTP method đúng ngữ nghĩa, status code mang ý nghĩa và message tự mô tả qua JSON cùng các header HTTP. Mỗi request chứa đủ thông tin xác thực nên phù hợp với stateless; `GET` có cơ chế cache; client cũng không cần biết request đi thẳng tới server hay qua CDN/gateway. Code on Demand không được dùng nhưng đây là ràng buộc tùy chọn.

GitHub còn trả các URL liên quan trong JSON, nhưng client vẫn phải dựa nhiều vào tài liệu để biết thao tác tiếp theo. API chưa có HATEOAS đầy đủ nên gọi đây là **RESTful-ish/resource-oriented API** hơn là RESTful.

## Tài liệu tham khảo

1. [GitHub REST API](https://docs.github.com/en/rest/issues/issues?apiVersion=2026-03-10)
