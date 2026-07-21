# Sử dụng Python 3.11 bản nhẹ
FROM python:3.11-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Copy file thư viện và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy file code app.py vào
COPY . .

# Lệnh BẮT BUỘC để giữ Streamlit chạy liên tục
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]