import os
import gmaps
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import fitparse
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy as np
from fit_tool.fit_file import FitFile
from fit_tool.profile.messages.record_message import RecordMessage


GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_PLATFORM_API_KEY')

FILE_LIST_PART1 = [
    'vulcanraven862_138103748459.fit',
    'vulcanraven862_138103749120.fit',
    'vulcanraven862_138104825005.fit',
    'vulcanraven862_138104825722.fit',
    'vulcanraven862_138104826049.fit',
    'vulcanraven862_138104827017.fit',
    'vulcanraven862_138171633574.fit',
    'vulcanraven862_138171633879.fit',
    'vulcanraven862_138171635729.fit',
    'vulcanraven862_138688209234.fit',
    'vulcanraven862_138688405981.fit',

    'vulcanraven862_138688416368.fit',
    'vulcanraven862_138688436252.fit',
    'vulcanraven862_138688574890.fit',
    'vulcanraven862_138688696297.fit',
    'vulcanraven862_138688702658.fit',
    'vulcanraven862_138688723619.fit',
    'vulcanraven862_138688743022.fit',
    'vulcanraven862_138688762875.fit',
    'vulcanraven862_138688773661.fit',
    'vulcanraven862_138688774054.fit',
    'vulcanraven862_138688774393.fit',
    'vulcanraven862_138688774722.fit',
]

FILE_LIST = [
    'vulcanraven862_214716667952.fit',
]


#DATA_PATH='/data/UploadedFiles_0-_Part2'
DATA_PATH='/data/UploadedFiles_0-_Part3'
IMAGE_PATH='/data/output-files'
OUT_PATH = f'{IMAGE_PATH}/vulcanraven862_138688405981.csv'
PNG_PATH = f'{IMAGE_PATH}/vulcanraven862_138688405981.png'
FIT_FILE_LIST = [FitFile.from_file(f'{DATA_PATH}/{filename}') for filename in FILE_LIST]


def main():
    play_with_cartopy()


def main2():
    positions_df = collect_fit_files_to_dataframe(FIT_FILE_LIST)

    central_longitude = positions_df['longitude'].mean()
    central_latitude = positions_df['latitude'].mean()
    
    gmaps.configure(api_key=GOOGLE_MAPS_API_KEY)

    fig = gmaps.figure(
        center=(central_latitude, central_longitude),
        zoom_level=5,
    )

    layer = gmaps.marker_layer(positions_df[['latitude', 'longitude']])
    fig.add_layer(layer)

    plt.savefig(PNG_PATH)



def play_with_cartopy():
    positions_df = collect_fit_files_to_dataframe(FIT_FILE_LIST)

    central_longitude = positions_df['longitude'].mean()
    central_latitude = positions_df['latitude'].mean()
    
    # Create a map using the Lambert Conformal Conic projection
    # projection = ccrs.LambertConformal(central_longitude=central_longitude, central_latitude=central_latitude)
    projection = ccrs.TransverseMercator(central_longitude=central_longitude, central_latitude=central_latitude, scale_factor=0.05)
    fig, ax = plt.subplots(subplot_kw={'projection': projection})

    delta = 0.1
    map_extent = [
        central_longitude - delta,
        central_longitude + delta,
        central_latitude - delta,
        central_latitude + delta,
    ]
    ax.set_extent(map_extent)

    
    # Use tiles from ArcGIS
    tiler = cimgt.GoogleTiles(style='satellite')
    ax.add_image(tiler, 10)  # The integer value (8) defines the zoom level

    fit_file_positions = [(row['longitude'], row['latitude']) for _, row in positions_df.iterrows()]
    # Plot the segment of the Colorado River
    ax.plot([p[0] for p in fit_file_positions], [p[1] for p in fit_file_positions], '-o', color='blue', linewidth=3, transform=ccrs.PlateCarree())

    ax.legend(loc="upper left")

    # Display the map
    plt.title("stealthybouncer's adventures in UTAH!!")
    # plt.show()
    plt.savefig(PNG_PATH)



def collect_fit_files_to_dataframe(fit_file_list: list
) -> DataFrame:

    full_trip = [positions for fit_file in fit_file_list for positions in get_fit_file_positions_and_altitude(fit_file)]

    return pd.DataFrame(full_trip, columns=['timestamp', 'longitude', 'latitude']).sort_values(by='timestamp')


def get_fit_file_positions_and_altitude(fit_file) -> list:
    # Load the FIT file
    positions = []

    for record in fit_file.records:
        message = record.message
        if isinstance(message, RecordMessage):
            positions.append((message.timestamp, message.position_long, message.position_lat))

    return positions


def play_with_cartopy1():
    # Approximate coordinates for a segment of the Colorado River through the Grand Canyon
    lats_river = [36.1, 36.0, 35.9, 35.8]
    lons_river = [-112.1, -112.2, -112.3, -112.4]

    # Coordinates for a hike into Havasu Creek, a side canyon
    lat_hike = 36.2551
    lon_hike = -112.6979

    # Create a map using the Lambert Conformal Conic projection
    projection = ccrs.LambertConformal(central_longitude=-112.0, central_latitude=36.0)
    fig, ax = plt.subplots(subplot_kw={'projection': projection})
    ax.set_extent([-113, -111, 35.5, 36.5])

    # Use tiles from ArcGIS
    tiler = cimgt.GoogleTiles()
    ax.add_image(tiler, 8)  # The integer value (8) defines the zoom level

    # Plot the segment of the Colorado River
    ax.plot(lons_river, lats_river, color='blue', linewidth=3, transform=ccrs.PlateCarree())

    # Plot the hike into Havasu Creek
    ax.scatter(lon_hike, lat_hike, color='red', s=100, transform=ccrs.PlateCarree(), label="Hike to Havasu Creek")
    ax.legend(loc="upper left")

    # Display the map
    plt.title("Colorado River and Hike into Havasu Creek")
    # plt.show()
    plt.savefig(PNG_PATH)


def play_with_mplot():
    mpl.style.use('seaborn')

    print('Start file read')
    
    FIT_FILE_LIST.to_csv(OUT_PATH)

    timestamp1 = []
    power1 = []
    distance1 = []
    speed1 = []
    cadence1 = []
    positions = []
    for record in FIT_FILE_LIST.records:
        message = record.message
        if isinstance(message, RecordMessage):
            timestamp1.append(message.timestamp)
            power1.append(message.power)
            distance1.append(message.distance)
            speed1.append(message.speed)
            cadence1.append(message.cadence)
            positions.append((message.position_long, message.position_lat))

    # print(timestamp1)

    start_time = timestamp1[0]
    time1 = np.array(timestamp1)
    power1 = np.array(power1)
    speed1 = np.array(speed1)
    cadence1 = np.array(cadence1)
    time1 = (time1 - start_time) / 1000 # seconds

    ax1 = plt.subplot(311)
    ax1.plot(time1, power1, '-o', label='app [W]')
    ax1.legend(loc='upper right')
    plt.xlabel('time (s)')
    plt.ylabel('power (W)')

    plt.subplot(312, sharex=ax1)
    plt.plot(time1, speed1, '-o', label='app [m/s]')
    plt.legend(loc='upper right')
    plt.xlabel('time (s)')
    plt.ylabel('speed (m/s)')

    plt.subplot(313, sharex=ax1)
    plt.plot(time1, cadence1, '-o', label='app [rpm]')
    plt.legend(loc='upper right')
    plt.xlabel('time (s)')
    plt.ylabel('cadence (rpm)')

    # plt.show()
    plt.savefig(PNG_PATH)

    # plot route of the contents of positions
    plt.figure()
    plt.plot([p[0] for p in positions], [p[1] for p in positions], '-o')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    # overlay onto a map
    # https://stackoverflow.com/questions/36008648/plot-data-on-top-of-a-map-using-python

    plt.savefig(PNG_PATH)


if __name__ == '__main__':
    main()
