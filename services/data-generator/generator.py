from datetime import datetime, timedelta
from faker import Faker
import random
from typing import List, Tuple, Any
from utils import PostgresClient
class TransactionGenerator:
    """Class chuyên đảm nhiệm việc sinh dữ liệu giao dịch và các kịch bản gian lận."""
    
    def __init__(self):
        self.fake = Faker()
        self.payment_methods = ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER']

    def _create_transaction(self, user: str = None, user_dest: str = None, 
                          amount: int = None, method: str = None, 
                          time_offset_seconds: int = 0) -> Tuple[Any, ...]:
        """Hàm dùng chung (Private) để tạo 1 record giao dịch, cho phép ghi đè tham số."""
        step = random.randint(1, 744)
        transaction_id = f"T{self.fake.random_number(digits=22)}"
        
        # Nếu không truyền tham số, sẽ lấy random theo chuẩn bình thường
        amount = amount or random.randint(100_000, 5_000_000)
        method = method or random.choice(self.payment_methods)
        
        user = user or f"user_{random.randint(1000, 10000)}"
        user_dest = user_dest or f"user_{random.randint(1000, 9999)}"
        while user == user_dest:
            user_dest = f"user_{random.randint(1000, 10000)}"
            
        # Tính toán thời gian (hỗ trợ cộng thêm giây để tạo kịch bản giao dịch liên tiếp)
        base_time = self.fake.date_time_this_month()
        tx_time = base_time + timedelta(seconds=time_offset_seconds)

        return (step, transaction_id, user, user_dest, amount, method, tx_time)

    # ==========================================
    # CÁC KỊCH BẢN SINH DỮ LIỆU
    # ==========================================

    def generate_normal_batch(self, batch_size: int = 10) -> List[Tuple[Any, ...]]:
        """Kịch bản 1: Sinh dữ liệu giao dịch hoàn toàn bình thường ngẫu nhiên."""
        return [self._create_transaction() for _ in range(batch_size)]

    def generate_velocity_fraud(self, num_transactions: int = 5) -> List[Tuple[Any, ...]]:
        """Kịch bản 2: Velocity Fraud - 1 user thực hiện nhiều giao dịch liên tiếp cách nhau 1-2 giây."""
        hacker_user = f"user_{random.randint(1000, 10000)}"
        transactions = []
        
        for i in range(num_transactions):
            # Thời gian nhích lên 2 giây cho mỗi giao dịch
            tx = self._create_transaction(
                user=hacker_user, 
                amount=random.randint(50_000, 200_000), # Chia nhỏ tiền để không bị chú ý
                method='TRANSFER',
                time_offset_seconds=(i * 2) 
            )
            transactions.append(tx)
            
        return transactions

    def generate_scattering_fraud(self, num_destinations: int = 10) -> List[Tuple[Any, ...]]:
        """Kịch bản 3: Phân tán tiền - 1 user chuyển tiền cho hàng loạt user khác nhau cùng lúc."""
        compromised_user = f"user_{random.randint(1000, 10000)}"
        transactions = []
        
        for _ in range(num_destinations):
            tx = self._create_transaction(
                user=compromised_user,
                method='TRANSFER',
                time_offset_seconds=random.randint(0, 5) # Diễn ra gần như cùng 1 thời điểm
            )
            transactions.append(tx)
            
        return transactions

    def generate_massive_fraud(self) -> List[Tuple[Any, ...]]:
        """Kịch bản 4: Giao dịch rút tiền đột biến, số tiền khổng lồ."""
        tx = self._create_transaction(
            amount=random.randint(500_000_000, 2_000_000_000), # Từ 500 triệu đến 2 tỷ
            method='CASH_OUT'
        )
        return [tx]

    def generate_mixed_batch(self, total_size: int = 100) -> List[Tuple[Any, ...]]:
        """Tạo một batch hỗn hợp chứa cả data thật và các luồng gian lận (để test hệ thống)."""
        data = []
        
        # 80% dữ liệu bình thường
        normal_count = int(total_size * 0.8)
        data.extend(self.generate_normal_batch(normal_count))
        
        # 20% dữ liệu gian lận các loại
        data.extend(self.generate_velocity_fraud(num_transactions=5))
        data.extend(self.generate_scattering_fraud(num_destinations=10))
        data.extend(self.generate_massive_fraud())
        data.extend(self.generate_massive_fraud())
        
        # Xáo trộn mảng dữ liệu để hệ thống xử lý stream nhận vào một cách ngẫu nhiên
        random.shuffle(data)
        return data
    
class DataIngestionPipeline:
    """Class quản lý luồng đẩy dữ liệu vào các hệ thống lưu trữ khác nhau."""
    
    def __init__(self, sql_filepath: str = "insert_transaction.sql"):
        self.sql_filepath = sql_filepath
        self.generator = TransactionGenerator() # Composition: Nhúng generator vào pipeline

    def _read_sql_file(self) -> str:
        """Đọc file SQL an toàn và tự động đóng file."""
        try:
            with open(self.sql_filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Không tìm thấy file SQL tại đường dẫn: {self.sql_filepath}")

    def import_data_to_postgres(self, batch_size: int = 10) -> None:
        """Sinh dữ liệu và đẩy vào PostgreSQL thông qua class PostgresClient."""
        transactions = self.generator.generate_mixed_batch(batch_size)
        insert_sql = self._read_sql_file()
        
        # Tái sử dụng Context Manager của PostgresClient từ ví dụ trước
        with PostgresClient(host="postgres", database="finhouse", user="finhouse", password="finhouse") as db:
            db.executemany(insert_sql, transactions)
            
        print(f"📦 Đã đẩy thành công {batch_size} records vào PostgreSQL.")

    def import_data_to_minio(self, batch_size: int = 10) -> None:
        """Sinh dữ liệu và đẩy vào MinIO dưới dạng Object (CSV/Parquet)."""
        transactions = self.generator.generate_mixed_batch(batch_size)
        
        # Todo: Tích hợp thư viện minio hoặc boto3 tại đây. 
        # Thường sẽ cần dùng Pandas để convert danh sách transactions thành file Parquet trước khi upload.
        print("⏳ Logic đẩy file lên MinIO đang được phát triển...")
        

# ==========================================
# KHU VỰC THỰC THI (ENTRY POINT)
# ==========================================
if __name__ == "__main__":
    # Khởi tạo Pipeline
    while True:
        pipeline = DataIngestionPipeline(sql_filepath="sql/insert_transaction.sql")
        
        # Kích hoạt luồng đẩy dữ liệu
        pipeline.import_data_to_postgres(batch_size=50)
        pipeline.import_data_to_minio(batch_size=50)