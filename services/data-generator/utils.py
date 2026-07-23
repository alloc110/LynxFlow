import psycopg2
from psycopg2 import Error
from typing import List, Tuple, Any, Optional

class PostgresClient:
    def __init__(self, host: str = "postgres", port: str = "5432", 
                 database: str = "finhouse", user: str = "finhouse", 
                 password: str = "finhouse"):
        """Khởi tạo các tham số cấu hình kết nối."""
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection: Optional[psycopg2.extensions.connection] = None
        self.cursor: Optional[psycopg2.extensions.cursor] = None

    def connect(self, retries: int = 5, delay: int = 3) -> None:
        """Thiết lập kết nối với cơ chế tự động thử lại nếu DB chưa sẵn sàng."""
        for attempt in range(1, retries + 1):
            try:
                self.connection = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                self.cursor = self.connection.cursor()
                print(f"🟢 Đã kết nối thành công tới PostgreSQL ở lần thử {attempt}.")
                return # Thoát vòng lặp nếu thành công
                
            except psycopg2.OperationalError as e:
                print(f"⏳ Thử kết nối lần {attempt}/{retries} thất bại. Chờ {delay}s...")
                if attempt == retries:
                    print("🔴 Không thể kết nối sau nhiều lần thử.")
                    raise e
                time.sleep(delay)
                
    
    def executemany(self, query: str, data: List[Tuple[Any, ...]]) -> None:
        """
        Thực thi lệnh SQL với danh sách dữ liệu (Bulk insert/update).
        Có đi kèm cơ chế commit và rollback để đảm bảo an toàn dữ liệu.
        """
        if not self.cursor or not self.connection:
            raise ConnectionError("Chưa có kết nối DB. Vui lòng gọi hàm connect() trước.")
        
        try:
            self.cursor.executemany(query, data)
            self.connection.commit()  # Bắt buộc phải có để lưu thay đổi vào DB
            print(f"✅ Đã thực thi thành công {self.cursor.rowcount} dòng.")
            
        except Error as e:
            self.connection.rollback() # Hoàn tác nếu có lỗi xảy ra ở bất kỳ dòng nào
            print(f"🔴 Lỗi khi thực thi executemany: {e}")
            raise e

    def disconnect(self) -> None:
        """Đóng cursor và giải phóng connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("⚪ Đã đóng kết nối PostgreSQL.")

    # --- Hỗ trợ Context Manager (with statement) ---
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()