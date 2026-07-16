variable "project_id" {
  description = "ID của Google Cloud Project"
  type        = string
  default     = "fraud-transaction-2026" # Điền ID thực tế trên GCP của bạn vào đây
}

variable "region" {
  description = "Region triển khai tài nguyên"
  type        = string
  default     = "asia-southeast1" # Singapore, độ trễ tốt nhất
}


variable "db_password" {
  description = "Mật khẩu cho user database mặc định"
  type        = string
  sensitive   = true
  default     = "password"
}