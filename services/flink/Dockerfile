FROM flink:1.18.1-scala_2.12

# Tải Flink SQL Kafka Connector tương thích với Flink 1.18
RUN wget -P /opt/flink/lib/ https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.1-1.18/flink-sql-connector-kafka-3.0.1-1.18.jar

# Tải Flink JDBC Connector cho Flink 1.18 (phiên bản 3.1.2-1.18 tương thích tốt)
RUN wget -P /opt/flink/lib/ https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.2-1.18/flink-connector-jdbc-3.1.2-1.18.jar

# Tải PostgreSQL JDBC Driver
RUN wget -P /opt/flink/lib/ https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.1/postgresql-42.7.1.jar