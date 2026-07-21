# Sử dụng base image Ubuntu 22.04 để đồng bộ kiến trúc với frontend
FROM ubuntu:22.04

# Vô hiệu hóa các prompt hỏi (như chọn múi giờ) trong quá trình cài đặt gói
ENV DEBIAN_FRONTEND=noninteractive

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Cài đặt PPA để lấy Python 3.11, cùng các thư viện hệ thống cần thiết cho psycopg2 (libpq-dev, gcc)
RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements vào trước để tận dụng Docker cache
COPY requirements.txt .

# Cài đặt thư viện Python (Sử dụng --ignore-installed để tránh lỗi đụng độ gói hệ thống)
RUN python3.11 -m pip install --no-cache-dir --ignore-installed -r requirements.txt

# Copy toàn bộ code nguồn vào container
COPY . .

# Khai báo port của FastAPI
EXPOSE 8001

# Chạy FastAPI bằng Uvicorn trên port 8001 (Gọi đích danh python3.11)
CMD ["python3.11", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]