FROM quay.io/debezium/connect:2.5.4.Final

USER root
RUN microdnf -y install unzip && microdnf clean all

USER kafka
RUN mkdir -p /kafka/connect/redis-sink && \
    cd /kafka/connect/redis-sink && \
    curl -sL "https://api.hub.confluent.io/api/plugins/redis/redis-kafka-connect/versions/0.9.0/archive" -o redis-plugin.zip && \
    unzip redis-plugin.zip && \
    # Vào đúng thư mục giải nén để lấy file .jar mang ra ngoài
    mv redis-redis-kafka-connect-0.9.0/lib/*.jar . && \
    # Xóa sạch thư mục rác và file zip
    rm -rf redis-redis-kafka-connect-0.9.0 redis-plugin.zip