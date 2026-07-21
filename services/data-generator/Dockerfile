# Sử dụng base image Ubuntu 22.04 
FROM ubuntu:22.04

# Vô hiệu hóa các prompt hỏi trong quá trình cài đặt gói
ENV DEBIAN_FRONTEND=noninteractive

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Cài đặt PPA lấy Python 3.11 và các thư viện hệ thống cần thiết
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

# Cài đặt thư viện Python (kèm cờ --ignore-installed)
RUN python3.11 -m pip install --no-cache-dir --ignore-installed -r requirements.txt

# Copy toàn bộ code nguồn vào container
COPY . .

# Lệnh chạy file script sinh dữ liệu (Thay 'generator.py' bằng tên file thực tế của bạn)
CMD ["python3.11", "generator.py"]