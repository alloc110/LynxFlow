# ==========================================
# 1. Google Cloud Storage (Data Lake / Checkpoints)
# ==========================================
resource "google_storage_bucket" "data_lake" {
  name          = "${var.project_id}-data-lake"
  location      = var.region
  force_destroy = true # Cho phép xóa bucket dev kể cả khi có data bên trong

  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

# ==========================================
# 2. Pub/Sub (Messaging / Streaming)
# ==========================================
resource "google_pubsub_topic" "cdc_events" {
  name = "cdc-events"
}

resource "google_pubsub_subscription" "flink_processor" {
  name  = "flink-processor-sub"
  topic = google_pubsub_topic.cdc_events.name

  # Giữ tin nhắn trong 3 ngày nếu Flink bị chết
  message_retention_duration = "259200s" 
  retain_acked_messages      = false
  ack_deadline_seconds       = 20
}

# ==========================================
# 3. Cloud SQL (PostgreSQL - Database chính)
# ==========================================
resource "google_sql_database_instance" "primary" {
  name             = "pg-primary"
  database_version = "POSTGRES_15"
  region           = var.region

  # Quan trọng cho môi trường dev: Cho phép xóa db dễ dàng
  deletion_protection = false 

  settings {
    tier = "db-f1-micro" # Cấu hình nhỏ nhất cho dev để tiết kiệm
    
    # Cấu hình IP Public (Cho dev dễ kết nối. Lên prod nên dùng Private IP)
    ip_configuration {
      ipv4_enabled = true
    }
  }
}

resource "google_sql_database" "default_db" {
  name     = "app_database"
  instance = google_sql_database_instance.primary.name
}

resource "google_sql_user" "default_user" {
  name     = "admin"
  instance = google_sql_database_instance.primary.name
  password = var.db_password
}

# ==========================================
# 4. GKE Autopilot (Chạy Flink & Airflow)
# ==========================================
resource "google_container_cluster" "autopilot_cluster" {
  name     = "data-platform-cluster"
  location = var.region

  # Chìa khóa để bật chế độ Autopilot (Serverless K8s)
  enable_autopilot = true

  # Cấu hình mạng mặc định
  network    = "default"
  subnetwork = "default"

  # Tắt bảo vệ xóa để dễ dàng destroy ở môi trường dev
  deletion_protection = false
}