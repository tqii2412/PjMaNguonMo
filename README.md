# Website Bán Trái Cây
Đây là một dự án website bán trái cây sử dụng **Python (Django)** cho backend, **Vue.js** cho frontend và **MySQL** cho cơ sở dữ liệu. Dự án này cho phép người dùng duyệt qua các loại trái cây, xem chi tiết sản phẩm, và thực hiện các giao dịch mua bán.
## Môi Trường Phát Triển

| Thành phần               | Phiên bản     |
|--------------------------|---------------|
| Python                   | 3.13.2        |
| Django                   | 5.1.6         |
| Django Rest Framework    | 3.15.2        |
| MySQL                    | 8.0           |
| Vue.js                   | @vue/cli 5.0.8 |
| Hệ điều hành             | Windows 10 Pro|
| IDE sử dụng              | VS Code       |
## Cài Đặt Dự Án
###2. Cài Đặt Môi Trường Ảo (Python)

a. Tạo Môi Trường Ảo:
python -m venv venv
b. Kích Hoạt Môi Trường Ảo:
- Trên windows:
.\venv\Scripts\activate
-Trên macOS/Linux:
source venv/bin/activate

###3. Cài Đặt Các Phụ Thuộc Python:
Sau khi kích hoạt môi trường ảo, cài đặt các thư viện cần thiết từ tệp requirements.txt:
pip install -r requirements.txt

###4. Cài Đặt MySQL
a.Tạo database trong MySQL:
CREATE DATABASE fruit_shop;
b. Cập nhật thông tin kết nối database trong tệp settings.py của Django:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fruit_shop',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

###5. Cài Đặt Vue.js (Frontend)
a. Cài Đặt Node.js và Vue CLI
Cài đặt Node.js và Vue CLI. Sau đó, bạn có thể cài đặt các thư viện frontend của dự án:

npm install

b. Chạy Server Frontend
Sau khi cài đặt các phụ thuộc frontend, bạn có thể chạy server Vue.js:

npm run serve

###6. Migrate Database (Django)

python manage.py migrate

###7. Chạy Dự Án Django
 
python manage.py runserver

###8. Kiểm Tra Dự Án
Mở trình duyệt và truy cập địa chỉ http://127.0.0.1:8000 để kiểm tra ứng dụng Django.
Frontend (Vue.js) sẽ chạy trên cổng 8080, và bạn có thể truy cập nó tại http://127.0.0.1:8080.

## Lưu Ý Quan Trọng

1. **Thay Đổi Cổng Frontend (Vue.js)**:
   Khi bạn chạy ứng dụng Vue.js bằng lệnh `npm run serve`, Vue CLI sẽ khởi động frontend của bạn trên một cổng (port) nhất định, mặc định là **8080**. Tuy nhiên, nếu cổng này đã bị chiếm dụng bởi một ứng dụng khác, Vue CLI sẽ tự động chọn cổng khác (ví dụ: 3000, 8081, v.v...). Bạn cần chắc chắn rằng cổng frontend trong cấu hình **CORS** của Django phải khớp với cổng mà Vue.js đang chạy.

2. **Cập Nhật CORS trong Django**:
   Trong tệp `settings.py` của Django, bạn cần cập nhật danh sách `CORS_ALLOWED_ORIGINS` để bao gồm địa chỉ và cổng mà frontend của bạn đang sử dụng. Nếu bạn chạy Vue.js trên cổng **8080** (hoặc cổng khác), hãy đảm bảo rằng các địa chỉ sau được thêm vào:
```python
   CORS_ALLOWED_ORIGINS = [
       "http://127.0.0.1:8000",  # Cổng Django
       "http://localhost:8080",   # Cổng của Vue.js
       "http://192.168.1.6:8080", # Nếu bạn chạy Vue.js trên một máy khác trong mạng LAN
   ]
Kiểm Tra Cổng của Vue.js: Khi bạn chạy Vue.js, terminal sẽ thông báo cổng mà ứng dụng đang sử dụng. Ví dụ:
App running at:
- Local:   http://localhost:8080/
- Network: http://192.168.1.6:8080/

Hãy đảm bảo rằng địa chỉ và cổng frontend này đã được thêm vào cấu hình CORS_ALLOWED_ORIGINS của Django.

