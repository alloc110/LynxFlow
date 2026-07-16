# LynxFlow

```
├── .vscode/                    # Cấu hình IDE chung cho team
│   ├── extensions.json         # Danh sách các extension khuyên dùng
│   └── settings.json           # Cấu hình linting, formatting mặc định
├── infrastructure/             # Infrastructure as Code (IaC)
│   ├── modules/                # Các module Terraform dùng chung
│   ├── environments/           # Cấu hình riêng theo môi trường
│   │   ├── dev/
│   │   └── prod/
│   └── backend.tf
├── kubernetes/                 # Các tệp cấu hình triển khai ứng dụng
│   ├── base/                   # Manifests cốt lõi (Kafka, ClickHouse, Postgres, v.v.)
│   ├── overlays/               # Ghi đè cấu hình cho dev/prod (nếu dùng Kustomize)
│   └── helm-values/            # Custom values cho các Helm charts (Airflow, Flink...)
├── pipelines/                  # Logic xử lý dữ liệu lõi
│   ├── flink-jobs/             # Chứa source code Java/Scala cho xử lý realtime
│   │   ├── pom.xml / build.gradle
│   │   └── src/main/java/...
│   ├── cdc-configs/            # Cấu hình cho Debezium / Kafka Connectors
│   │   └── postgres-source.json
│   └── spark-jobs/             # Code Python/Scala cho xử lý Batch
├── dags/                       # Apache Airflow DAGs (Điều phối)
│   ├── core_jobs/              # Các pipeline xử lý chính
│   ├── utils/                  # Các hàm tiện ích dùng chung cho DAGs
│   └── .airflowignore          # Bỏ qua các file không cần parse
├── tests/                      # Tích hợp kiểm thử (Integration & Unit Tests)
│   ├── test_dags/              # Test cho Airflow DAGs
│   └── test_pipelines/         # Test cho logic xử lý dữ liệu
├── ci-cd/                      # Scripts phục vụ tự động hóa
│   ├── docker/                 # Các Dockerfile build image cho Spark/Flink
│   └── Jenkinsfile             # Hoặc thư mục .github/workflows
├── docs/                       # Tài liệu kiến trúc, data catalog
├── .env.example                # Template chứa các biến môi trường
├── .gitignore
└── README.md                   # Hướng dẫn setup dự án tổng quan
```
