from fastapi import FastAPI,HTTPException
from models.Producer import Producer
from models.Topic import Topic
from models.Consumer import Consumer
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from functional import seq

app = FastAPI()

Instrumentator().instrument(app).expose(app)

topics = seq(
        Topic('1', Producer("Producer 1"), [Consumer("My consumer 1"), Consumer("My consumer 2")]),
        Topic('2', Producer("My producer 2"), [Consumer("My consumer 3"), Consumer("My consumer 4")])
)


def search_in_topics(name: str):
    return topics.find(lambda topic: topic.name == name)


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/topics")
async def get_topics():
    return JSONResponse(jsonable_encoder(topics))


@app.get("/topics/{name}")
async def get_topic(name):
    topic = search_in_topics(name)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    else:
        return JSONResponse(jsonable_encoder(topic))



