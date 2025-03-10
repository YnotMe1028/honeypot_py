# honeypot_py

## Giới thiệu

Dự án này là một **SSH Honeypot** đơn giản được viết bằng Python sử dụng thư viện `Paramiko`. Nó giả lập một máy chủ SSH để thu thập thông tin từ các cuộc tấn công brute-force hoặc các truy cập không hợp lệ. Dự án này được xây dựng cho mục đích học tập và nghiên cứu bảo mật cá nhân.

## Chức năng chính

- Giả lập một máy chủ SSH chạy trên `localhost` với một banner giống như hệ thống Ubuntu.
- Ghi lại mọi nỗ lực đăng nhập cùng với tên đăng nhập và mật khẩu đã thử.
- Cung cấp một môi trường giả lập Shell đơn giản để tương tác với kẻ tấn công.
- Ghi lại tất cả các lệnh mà kẻ tấn công đã thực thi.

## Cách sử dụng

### Cài đặt

1. **Clone repo về máy của bạn**:

```bash
git clone https://github.com/YnotMe1028/honeypot_basic.git
```

2. **Cài đặt các thư viện cần thiết**:

```bash
pip install -r requirements.txt
```

3. **Tạo một khóa RSA để dùng cho SSH server**:

```bash
ssh-keygen -t rsa -b 2048 -f server.key
```

### Chạy chương trình

Bạn có thể chạy honeypot với lệnh sau:

```bash
python honeypy.py -a 127.0.0.1 -p 2810 -s
```

## Tệp cấu trúc

- `ssh_honeypot.py`: Chứa toàn bộ logic của SSH Honeypot.
- `honeypy.py`: Tập lệnh chính dùng để khởi chạy Honeypot
- `requirements.txt`: Danh sách các thư viện cần thiết để chạy dự án.
- `audits.log`: Ghi lại thông tin về các nỗ lực đăng nhập.
- `cmd_audits.log`: Ghi lại các lệnh được thực thi.

