from typing import Union, List
import redis
from fastapi import FastAPI
from . import data_processing as dp
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
def read_root_hits():
    r.incr('hits')
    return {'number of hits': r.get('/hits')}


fit_file_path = f'/data/UploadedFiles_0-_Part3/vulcanraven862_214716667952.fit'


def get_coordinate_df() -> DataFrame:
    '''
    API endpoint to extract GPS data from a FIT file and return it as JSON.

    Returns:
        DataFrame: dataframe containing the coordinates listed in specified file
    '''
    gps_data = dp.get_gps_data_as_dataframe(DATA_PATH, FILE_LIST, )
    return gps_data


@app.get('/gps_data')
def get_gps_data() -> str:
    '''
    API endpoint to extract GPS data from a FIT file and return it as JSON.

    Returns:
        DataFrame: dataframe containing the coordinates listed in specified file
    '''
    gps_coord_df = dp.get_coordinate_df()
    return gps_coord_df.to_json()


@app.get('/get_gps_map')
def get_gps_map():
    """
    Returns a map of GPS coordinates.

    Uses the `get_coordinate_df()` function from the `dp` module to retrieve a DataFrame of GPS coordinates,
    and then passes it to the `map_coordinates()` function from the same module to generate a map.
    """
    gps_coord_df = dp.get_coordinate_df()
    dp.map_coordinates(gps_coord_df)
