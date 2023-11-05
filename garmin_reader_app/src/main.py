from typing import Union, List
import redis
from fastapi import FastAPI
from fit_file_reader import data_processing
import pandas as pd
from pandas import DataFrame

app = FastAPI()

r = redis.Redis(host='redis', port=6379)

FILE_LIST = [
    'vulcanraven862_214716583466.fit',
    'vulcanraven862_214716587217.fit',
    'vulcanraven862_214716591197.fit',
    'vulcanraven862_214716595045.fit',
    'vulcanraven862_214716601751.fit',
    'vulcanraven862_214716612798.fit',
    'vulcanraven862_214716619714.fit',
    'vulcanraven862_214716625911.fit',
    'vulcanraven862_214716630426.fit',
    'vulcanraven862_214716636529.fit',
    'vulcanraven862_214716645364.fit',

    'vulcanraven862_214716667952.fit',

    'vulcanraven862_214716678978.fit',
    'vulcanraven862_214716684220.fit',
    'vulcanraven862_208966175165.fit',

]
DATA_PATH='/data/UploadedFiles_0-_Part3'

@app.get("/hello")
def read_root():
    return {"Hello": "World1234"}

@app.get('/hits')
def read_root():
    r.incr('hits')
    return {'number of hits': r.get('/hits')}


fit_file_path = f'/data/UploadedFiles_0-_Part3/vulcanraven862_214716667952.fit'

@app.get('/gps_data')
def get_gps_data() -> str:
    '''
    API endpoint to extract GPS data from a FIT file and return it as JSON.

    Returns:
        DataFrame: dataframe containing the coordinates listed in specified file
    '''
    gps_data = data_processing.get_gps_data_as_dataframe(DATA_PATH, FILE_LIST, )
    return gps_data.to_json()

@app.get('/get_gps_map')
def get_gps_map():
    pass
