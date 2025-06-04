import pika
import json
import random
from datetime import datetime
from .fitness_coach_service import generate_and_store_wod

RABBITMQ_HOST = "rabbitmq"
QUEUE_NAME = "createWodQueue"

def callback(ch, method, properties, body):
    try:
        # Simulate 20% random failure
        if random.random() < 0.2:
            raise Exception("Random failure in WOD generation (simulated)")

        data = json.loads(body)
        user_id = data["user_id"]
        requested_at = data.get("requested_at", datetime.utcnow().isoformat())
        # Generate and persist WOD for the user
        generate_and_store_wod(user_id, requested_at)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def start_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=pika.PlainCredentials("rabbit", "docker"))
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print("Coach consumer started. Waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()