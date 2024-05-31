from kafka import KafkaConsumer, KafkaProducer

# Kafka 소비자 설정
consumer = KafkaConsumer('mysql-orders', bootstrap_servers='localhost:9092')

# Kafka 프로듀서 설정
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# 메시지 처리
for message in consumer:
    # 메시지 처리 로직 추가
    print(message)
    producer.send('processed-orders', message.value)