import os
import json
import pika
from .database import save_workout_stat

def callback(ch, method, properties, body):
    """Callback function to process incoming messages from RabbitMQ."""
    workout_data = json.loads(body)
    # Assuming workout_data contains the necessary fields
    save_workout_stat(workout_data)

def run_consumer():
    """Set up the RabbitMQ consumer to listen for workout.performed events."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST', 'localhost')))
    channel = connection.channel()

    channel.exchange_declare(exchange='workout.performed', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='workout.performed', queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()