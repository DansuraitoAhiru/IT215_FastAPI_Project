# Checklist Test API, Fix Bug và Hoàn thiện Swagger
## I. TEST API
### 1. Authentication
#### POST `/auth/register`
 Đăng ký với dữ liệu hợp lệ → `201 Created`
 Email đã tồn tại → `409 Conflict`
 Email sai format → `422 Unprocessable Entity`
 Password quá ngắn → `422 Unprocessable Entity`
 Thiếu email → `422 Unprocessable Entity`
 Thiếu password → `422 Unprocessable Entity`

#### POST `/auth/login`
 Đăng nhập đúng email/password → `200 OK`
 Sai email → `401 Unauthorized`
 Sai password → `401 Unauthorized`
 User không tồn tại → `401 Unauthorized`
 Thiếu dữ liệu → `422 Unprocessable Entity`
 User bị inactive → trả về status phù hợp
 Response không chứa `password` hoặc `password_hash`
 Access token được trả về đúng format


# 2. Research Project
## POST `/research-projects`
### Success
 User có quyền tạo project → tạo thành công
 Dữ liệu hợp lệ → `201 Created`
 Project được lưu đúng database
 `owner_id` được lấy từ user đang đăng nhập
 Không cho client tự ý thay đổi `owner_id`

### Error
 Chưa đăng nhập → `401 Unauthorized`
 Dữ liệu thiếu → `422 Unprocessable Entity`
 Dữ liệu không hợp lệ → `422 Unprocessable Entity`
 User không có quyền → `403 Forbidden`
 Lỗi nghiệp vụ không trả về `500`

## GET `/research-projects`
 User đăng nhập → lấy được danh sách project
 Chỉ trả về project mà user được phép xem
 Không làm lộ project của user khác
 Không đăng nhập → `401 Unauthorized`
 Không có dữ liệu → trả về `[]`
 Response đúng `response_model`

## GET `/research-projects/{id}`
### Success
 ID tồn tại và user có quyền → `200 OK`
 Response chứa đúng thông tin project

### Error
 ID không tồn tại → `404 Not Found`
 User không có quyền xem → `403 Forbidden`
 ID sai kiểu dữ liệu → `422 Unprocessable Entity`
 Chưa đăng nhập → `401 Unauthorized`


## PUT `/research-projects/{id}`
 Owner cập nhật project → thành công
 User không phải owner → `403 Forbidden`
 Project không tồn tại → `404 Not Found`
 Dữ liệu hợp lệ → cập nhật đúng DB
 Dữ liệu không hợp lệ → `422`
 Không cho sửa các field không được phép
 Không xảy ra `500`


## DELETE `/research-projects/{id}`
 Owner xóa project → thành công
 Project không tồn tại → `404 Not Found`
 User không phải owner → `403 Forbidden`
 Chưa đăng nhập → `401 Unauthorized`
 Project thực sự bị xóa khỏi DB
 Xử lý đúng dữ liệu liên quan nếu có Foreign Key


# 3. Research Task
## POST `/research-projects/{id}/research-tasks`
### Success
 Thành viên có quyền tạo task → `201 Created`
 Title hợp lệ
 Description hợp lệ
 Due date hợp lệ
 Priority hợp lệ
 Task được gắn đúng `project_id`
 Assignee hợp lệ nếu có

### Error
 Project không tồn tại → `404`
 User không thuộc project → `403`
 User không có quyền tạo task → `403`
 Thiếu title → `422`
 Priority không hợp lệ → `422`
 Assignee không tồn tại → `404`
 Assignee không thuộc project → `400/403`
 Project ID sai kiểu → `422`
 Không xảy ra Foreign Key `500`


## GET `/research-projects/{id}/research-tasks`
 User có quyền → lấy danh sách task
 Chỉ lấy task thuộc project tương ứng
 Không lộ task của project khác
 Project không tồn tại → `404`
 User không có quyền → `403`
 Không có task → `[]`
 Response đúng schema


## GET `/research-tasks/{task_id}`
 Task tồn tại → `200`
 Task không tồn tại → `404`
 User không có quyền → `403`
 Không lộ dữ liệu task ngoài phạm vi user được phép xem


## PUT `/research-tasks/{task_id}`
 User có quyền → cập nhật thành công
 Task không tồn tại → `404`
 User không có quyền → `403`
 Dữ liệu không hợp lệ → `422`
 Assignee không tồn tại → xử lý đúng
 Assignee không thuộc project → xử lý đúng
 Không xảy ra `500`


## DELETE `/research-tasks/{task_id}
 User có quyền → xóa thành công
 Task không tồn tại → `404`
 User không có quyền → `403`
 Task được xóa khỏi DB
 Không xảy ra `500`


# II. INTEGRATION TEST
## Luồng 1: Đăng ký → Đăng nhập
 Register user
 Login bằng tài khoản vừa tạo
 Nhận access token
 Dùng token gọi API protected

## Luồng 2: Tạo Project
 Login
 POST tạo project
 GET project vừa tạo
 Kiểm tra `owner_id`
 GET danh sách project
 PUT project
 DELETE project

## Luồng 3: Project → Task
 Tạo project
 Thêm thành viên
 Thành viên tạo task
 GET danh sách task
 PUT task
 DELETE task

## Luồng 4: Phân quyền
 Owner thực hiện chức năng được phép
 Member thực hiện chức năng được phép
 User ngoài project bị từ chối
 User chưa đăng nhập bị từ chối
 User không đủ quyền nhận `403`, không phải `500`


# III. FIX BUG
Sau mỗi lần integration test:
 Ghi lại API bị lỗi
 Ghi request gây lỗi
 Ghi status code thực tế
 Xác định nguyên nhân
 Sửa service/router/dependency/model tương ứng
 Test lại case lỗi
 Test lại case thành công
 Test thêm các case liên quan

### Các lỗi cần đặc biệt kiểm tra
 `IntegrityError` → xử lý và rollback transaction
 `NoResultFound` → trả `404`
 Object không tồn tại → không truy cập attribute trực tiếp
 Foreign Key sai → trả lỗi nghiệp vụ phù hợp
 Permission sai → `403`
 Authentication sai → `401`
 Validation sai → `422`
 Không để exception nghiệp vụ thông thường thành `500`
 Có `db.rollback()` khi transaction thất bại
 Không trả password/password_hash trong response
 Không để thông tin nội bộ database xuất hiện trong response


# IV. HOÀN THIỆN SWAGGER
## Router
Mỗi endpoint cần có:
 `summary`
 `description`
 `tags`
 `response_model`
 `status_code`

Ví dụ:
```python
@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo đề tài nghiên cứu",
    description="Tạo một đề tài nghiên cứu mới cho người dùng hiện tại.",
    tags=["Research Projects"]
)
def create_project(...):
    ...
```

## GET
```python
@router.get(
    "/{id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy thông tin đề tài nghiên cứu",
    description="Lấy thông tin một đề tài nghiên cứu theo ID.",
    tags=["Research Projects"]
)
```

## PUT
```python
@router.put(
    "/{id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
    summary="Cập nhật đề tài nghiên cứu",
    description="Cập nhật thông tin đề tài nghiên cứu.",
    tags=["Research Projects"]
)
```

## DELETE
```python
@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Xóa đề tài nghiên cứu",
    description="Xóa một đề tài nghiên cứu theo ID.",
    tags=["Research Projects"]
)
```

## Research Task
Dùng tag riêng:
```python
tags=["Research Tasks"]
```

Các API nên có summary rõ ràng:
 `Tạo nhiệm vụ nghiên cứu`
 `Lấy danh sách nhiệm vụ nghiên cứu`
 `Lấy thông tin nhiệm vụ nghiên cứu`
 `Cập nhật nhiệm vụ nghiên cứu`
 `Xóa nhiệm vụ nghiên cứu`


# V. CHECKLIST CUỐI CÙNG
### Test
 Tất cả API success case đều chạy
 Tất cả API error case đều chạy
 Authentication test xong
 Authorization test xong
 Validation test xong
 Integration test xong

### Bug
 Không còn `500` ở các case nghiệp vụ thông thường
 `401` dùng cho authentication
 `403` dùng cho permission
 `404` dùng cho resource không tồn tại
 `422` dùng cho validation
 `409` dùng cho conflict nếu có
 Database transaction được rollback khi lỗi

### Swagger
 Tất cả endpoint có `summary`
 Tất cả endpoint có `description`
 Tất cả endpoint có `tags`
 Tất cả endpoint có `response_model` phù hợp
 Status code được khai báo chính xác
 Schema request/response hiển thị đúng
 Không hiển thị các field nhạy cảm như password/password_hash
