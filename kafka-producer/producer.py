import setup
import os
import json
from time import sleep
from multiprocessing import Process
from kafka import KafkaConsumer

KAFKA_IP = os.getenv('KAFKA_IP', 'localhost')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9093')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'sales')


def produce(ip, port, topic, generate):
    producer = setup.create_kafka_producer(ip, port)
    message = generate()
    while True:
        try:
            producer.send(topic, json.dumps(next(message)).encode('utf8'))
            producer.flush()
            sleep(1)
        except Exception as e:
            print(f"Error: {e}")


def consume(ip, port, topic):
    consumer = KafkaConsumer(topic,
                             bootstrap_servers=ip + ':' + port,
                             auto_offset_reset='earliest',
                             group_id=None)
    try:
        while True:
            msg_pack = consumer.poll()
            if not msg_pack:
                sleep(1)
                continue
            for _, messages in msg_pack.items():
                for message in messages:
                    message = json.loads(message.value.decode('utf8'))
                    print(str(message))

    except KeyboardInterrupt:
        pass


def run(generate):
    # connect to kafka admin client and create topic
    setup.run(KAFKA_IP, KAFKA_PORT, KAFKA_TOPIC)
    # run a producer
    p1 = Process(target=lambda: produce(
        KAFKA_IP, KAFKA_PORT, KAFKA_TOPIC, generate))
    p1.start()
    # run a consumer
    #p2 = Process(target=lambda: consume(KAFKA_IP, KAFKA_PORT, KAFKA_TOPIC))
    # p2.start()

    p1.join()
    # p2.join()


if __name__ == "__main__":
    run()
