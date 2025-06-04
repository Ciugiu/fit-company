import pika
import json
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Literal
from datetime import datetime

CREATE_WOD_QUEUE = "createWodQueue"
DEAD_LETTER_QUEUE = "createWodQueue.dlq"
DEAD_LETTER_EXCHANGE = "createWodQueue.dlx"

def setup_queues():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq", credentials=pika.PlainCredentials("rabbit", "docker"))
    )
    channel = connection.channel()

    # Dead letter exchange and queue
    channel.exchange_declare(exchange=DEAD_LETTER_EXCHANGE, exchange_type='fanout', durable=True)
    channel.queue_declare(queue=DEAD_LETTER_QUEUE, durable=True)
    channel.queue_bind(exchange=DEAD_LETTER_EXCHANGE, queue=DEAD_LETTER_QUEUE)

    # Main queue with TTL, max length, and DLX
    args = {
        "x-message-ttl": 60000,  # 1 minute in ms
        "x-max-length": 100,
        "x-dead-letter-exchange": DEAD_LETTER_EXCHANGE,
        "x-dead-letter-routing-key": DEAD_LETTER_QUEUE,
    }
    channel.queue_declare(queue=CREATE_WOD_QUEUE, durable=True, arguments=args)

    connection.close()

class WodRequestMessage(BaseModel):
    user_id: str
    requested_at: datetime
    parameters: Optional[dict] = Field(default_factory=dict)
    difficulty: Optional[Literal["easy", "medium", "hard"]]
    goal: Optional[str]

def validate_wod_message(data):
    try:
        msg = WodRequestMessage(**data)
        return msg
    except ValidationError as e:
        raise ValueError(f"Invalid message format: {e}")

def on_message(channel, method, properties, body):
    try:
        data = json.loads(body)
        validate_wod_message(data)
        # ... process message ...
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        retries = properties.headers.get('x-retries', 0) if properties.headers else 0
        if retries < 3:
            headers = properties.headers or {}
            headers['x-retries'] = retries + 1
            channel.basic_publish(
                exchange='',
                routing_key=CREATE_WOD_QUEUE,
                body=body,
                properties=pika.BasicProperties(headers=headers)
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)
        else:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)