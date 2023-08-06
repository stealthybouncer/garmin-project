import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from fit_tool.fit_file import FitFile
from fit_tool.profile.messages.record_message import RecordMessage

DATA_PATH='/data/UploadedFiles_0-_Part2'

def main():
    mpl.style.use('seaborn')

    print('Start file read')
    fit_file = FitFile.from_file(f'{DATA_PATH}/vulcanraven862_138688405981.fit')
    
    out_path = f'{DATA_PATH}/vulcanraven862_138688405981.csv'
    fit_file.to_csv(out_path)

    timestamp1 = []
    power1 = []
    distance1 = []
    speed1 = []
    cadence1 = []
    for record in fit_file.records:
        message = record.message
        if isinstance(message, RecordMessage):
            timestamp1.append(message.timestamp)
            power1.append(message.power)
            distance1.append(message.distance)
            speed1.append(message.speed)
            cadence1.append(message.cadence)

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

    plt.show()


if __name__ == '__main__':
    main()
