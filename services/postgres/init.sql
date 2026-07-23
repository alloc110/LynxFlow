CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(100),
    amount BIGINT,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 3. Bảng Giao dịch (Nơi luồng data tuôn chảy liên tục)
DROP TABLE IF EXISTS transactions CASCADE;
CREATE TABLE transactions (
    step INT,
    transaction_id VARCHAR(50) PRIMARY KEY,
    source_user_id VARCHAR(50) REFERENCES users(user_id),
    dest_user_id VARCHAR(50) REFERENCES users(user_id),
    amount BIGINT,
    payment_method VARCHAR(50),
    transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Bảng Cảnh báo gian lận (Đích đến để Flink ghi kết quả)
CREATE TABLE fraud_alerts (
    transaction_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    amount DOUBLE PRECISION,
    payment_method VARCHAR(50),
    is_fraud_predicted INTEGER, -- Máy dự đoán (0 hoặc 1)
    
    -- HAI CỘT LỘC CẦN THÊM --
    actual_label INTEGER DEFAULT NULL, -- Con người xác nhận lại (0: Thật, 1: Gian lận)
    status VARCHAR(20) DEFAULT 'PENDING', -- Trạng thái (PENDING, VERIFIED, CLOSED)
    
    alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE users REPLICA IDENTITY FULL;
ALTER TABLE transactions REPLICA IDENTITY FULL;
ALTER TABLE fraud_alerts REPLICA IDENTITY FULL;

INSERT INTO users (user_id, full_name, amount, email)
SELECT 
    'user_' || id AS user_id,
    'User Name ' || id AS full_name, 
    (floor(random() * (50000000 - 100000 + 1)) + 100000)::bigint AS amount, -- Đã sửa thành ::bigint
    'user_' || id || '@example.com' AS email
FROM generate_series(1000, 10000) AS id
ON CONFLICT (user_id) DO NOTHING;