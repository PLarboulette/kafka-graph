from models.Consumer import Consumer
from models.Producer import Producer


class Topic:
    name: str
    producer: Producer
    consumers: []

    def __init__(self, name, producer: Producer, consumers):
        self.name = name
        self.producer = producer
        self.consumers = consumers
