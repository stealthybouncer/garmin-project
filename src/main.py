from typing import Union
import redis
from fastapi import FastAPI

app = FastAPI()

r = redis.Redis(host='redis', port=6379)


@app.get("/")
def read_root():
    return {"Hello": "World1234"}

@app.get('/hits')
def read_root():
    r.incr('hits')
    return {'number of hits': r.get('/hits')}
