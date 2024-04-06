from kafka import KafkaProducer
from kafka.producer.future import RecordMetadata


def kafka_send_message01():
    #    Example1: close를 호출해야 consumer에 데이터가 들어간다 ?

    producer = KafkaProducer(bootstrap_servers="localhost:19092")

    for _ in range(10):
        message = f"hello-{_}"
        producer.send("test-topic", message.encode())

    producer.close()


def kafka_send_message02():
    # Example 02: close를 호출하지 않고 Mesage를 보냄
    producer = KafkaProducer(bootstrap_servers="localhost:19092")

    for _ in range(10):
        future = producer.send("test-topic", b"hello")
        message = future.get(timeout=5)  # type: RecordMetadata
        print(message, type(message))
        producer.flush()


if __name__ == '__main__':
    kafka_send_message02()
