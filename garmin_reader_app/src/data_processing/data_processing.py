from fitparse import FitFile
import numpy as np
import pandas as pd
from pandas import DataFrame
from typing import List
from fit_tool.fit_file import FitFile
import folium
from folium.plugins import HeatMap

def get_gps_data_as_dataframe(
        folder_path: str,
        file_list: List[str],
        columns: list = ['timestamp', 'position_lat', 'position_long']
    ) -> DataFrame:
    '''
    Extracts gps data from a fit file and returns it as a pandas dataframe.
    
    Args:
        file_path: The path to the fit file.

    Returns:
        A pandas dataframe containing the gps data.
    '''
    # fit_file_list = [FitFile.from_file(f'{folder_path}/{filename}') for filename in file_list]
    file_paths = [f'{folder_path}/{filename}' for filename in file_list]
    # fit_file_list = [f'{folder_path}/{filename}' for filename in file_list]
    
    gps_data = []
    for file_path in file_paths:
        fit_file = FitFile(file_path)
        # with FitFile.from_file(file_path) as fit_file:
        for record in fit_file.get_messages('record'):
            entry = {}
            for record_data in record:
                if record_data.name == 'timestamp':
                    entry[record_data.name] = record_data.value.strftime('%Y-%m-%d %H:%M:%S.%f')
                elif (record_data.name == 'position_lat' or record_data.name == 'position_long'):
                    entry[record_data.name] = record_data.value
                entry[record_data.name] = record_data.value

            if all(cols in entry for cols in columns):
                gps_data.append(entry)
                
    gps_df = pd.DataFrame(gps_data, columns=columns)
    return gps_df.sort_values(by='timestamp',)

# write a function that takes a dataframe of coordinates and maps them
def map_coordinates(coordinates: DataFrame) -> None:
    '''
    Plots the coordinates on a map.
    
    Args:
        coordinates: A pandas dataframe containing the coordinates.
    '''
    # Create a map
    m = folium.Map(location=[coordinates['position_lat'].mean(), coordinates['position_long'].mean()], zoom_start=15)

    # Add a heatmap to the base map
    HeatMap(coordinates[['position_lat', 'position_long']], radius=10).add_to(m)

    # Display the map
    m.save('map.html')
