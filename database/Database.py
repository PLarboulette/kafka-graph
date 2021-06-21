from pyArango.connection import *
from pyArango.collection import Collection
from fastapi.encoders import jsonable_encoder

from models.Topic import Topic


def connect():
    connection = Connection(
        username="root",
        password="password"
    )

    if not connection.hasDatabase("topics"):
        connection.createDatabase(name="topics")

    db: Database = connection["topics"]

    if not db.hasCollection("topics"):
        db.createCollection(name="topics")

    return db["topics"]


def get_topics(topic_collection: Collection):
    return topic_collection.count()


def insert(topic_collection: Collection, topic: Topic):
    doc = topic_collection.createDocument()
    doc["name"] = topic.name
    doc['consumers'] = jsonable_encoder(topic.consumers)
    doc['producer'] = jsonable_encoder(topic.producer)
    doc.save()
    return 1


def search(topic_collection: Collection):
    example = {'name': "1"}
    query = topic_collection.fetchByExample(example, batchSize=20, count=True)
    return query.count

