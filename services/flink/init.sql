CREATE TABLE kafka_users (
    user_id STRING,
    full_name STRING,
    amount BIGINT,
    email STRING,
    created_at BIGINT,
    current_balance AS amount,
    PRIMARY KEY (user_id) NOT ENFORCED
) WITH (
    'connector' = 'kafka',
    'topic' = 'finhouse.public.users',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink_production_group',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'debezium-json',
    'debezium-json.schema-include' = 'true',
    'debezium-json.ignore-parse-errors' = 'true'
);