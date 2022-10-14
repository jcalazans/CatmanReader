from apread import APReader
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

input_file = "C:\\Users\\jcerqueira\\Desktop\\ST-21306-10_2_2-Bore_FAT_with_Water_TCN.BIN"

def app_read(input_file):
    reader = APReader(r'' + input_file + '')
    return reader

def interact_channels(function, reader, channel_selected='null', time_frame=1/864000):
    cname = []
    data_time = []
    data_index = []
    for group in reader.Groups:
        group_channels = group.ChannelsY
        for channel in group_channels:
            cname.append(channel.Name)
            if (channel.Name == channel_selected) and (channel.Name != 'null'):
                data = channel.data
                data_length = channel.length
                time = channel.extHeader['T0']
                unit = channel.extHeader['PhysUnit']
                for i in range(data_length):
                    time = time + time_frame
                    data_time.append(time)
                    data_index.append(i)
    if function == 'read_channels':
        return cname
    elif function == 'get_data':
        return data, data_index, data_time, unit

def select_channel(channels):
    for coption in channels:
        index = channels.index(coption)
        print(str(index) + ' - ' + coption)
    channel_selected = int(input('Selecione o numero do Canal Desejado:'))
    cname = channels[channel_selected]
    return cname

def get_frequency(reader):
    for channel in reader.Channels:
        if channel.Name == channel_selected:
            dt = channel.extHeader['dt']
    if dt == 100:
        freq = 10   # [Hz]
        time_frame = 1 / (24 * 3600 * 10)
        return freq, time_frame
    if dt == 3.3333333333333335:
        freq = 300  # [Hz]
        time_frame = 1 / (24 * 3600 * 300)
        return freq, time_frame

def statistics(data):
    max_data = np.max(data)
    min_data = np.min(data)
    mean_data = np.mean(data)
    dp_data = np.std(data)
    return max_data, min_data, mean_data, dp_data

def get_outlier(data, data_index):
    value_min = float(input('Qual o valor minimo de corte? '))
    value_max = float(input('Qual o valor maximo de corte? '))
    dic_index_data = dict(zip(data_index, data))
    outlier = []
    outlier_index = []
    for key_value, data_value in dic_index_data.items():
        if (data_value < value_min) or (data_value > value_max):
            outlier.append(data_value)
            outlier_index.append(key_value)
    return outlier, outlier_index

def floatHourToTime(fh):
    x = fh*24*3600*1000
    hours, hourSeconds = divmod(x, 3600*1000)
    minutes, minutesSeconds = divmod(hourSeconds, 60000)
    seconds, remainder = divmod(minutesSeconds, 1000)
    # milliseconds = int(1e3 * remainder)
    milliseconds = remainder
    if milliseconds < 10:
        milliseconds = 0  # compensate for rounding errors
    return (
        int(hours),
        int(minutes),
        int(seconds),
        int(milliseconds),
    )

def convert_time(time_list):
    time_datetime = []
    for time in time_list:
        dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(time) - 2)
        hour, minute, second, millisecond = floatHourToTime(time % 1)
        dt = dt.replace(hour=hour, minute=minute, second=second)
        time_datetime.append(dt)
    return time_datetime

def plot(data_time, data, channel_selected, unit):
    fig, ax = plt.subplots()
    # fig.suptitle(channel_selected)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%h-%d %H:%M:%S'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.plot(data_time, data, label=channel_selected + ' in ' + unit)
    # ax.set_ylabel(unit)
    ax.legend(loc='lower left', bbox_to_anchor = (0.0,1.0))
    ax.tick_params(axis='x',which='minor', labelrotation=45)
    plt.show()

# def get_equivalent_data(data_comparison, outlier_index):
#
#     for i in outlier_index:
#         data

reader = app_read(input_file)
channels = interact_channels('read_channels', reader)
channel_selected = select_channel(channels)
freq, time_frame = get_frequency(reader)
data, data_index, data_time, unit = interact_channels('get_data', reader, channel_selected, time_frame)
max_value, min_value, mean_channel, std_channel = statistics(data)
# print('O valor maximo de ' + str(channel_selected) + ' e: ' + str(max_value))
# print('O valor minimo de ' + str(channel_selected) + ' e: ' + str(min_value))
# print('A media +- 1 DP de ' + str(channel_selected) + ' e: ' + str(mean_channel) + ' +- ' + str(std_channel))
# print('A media +- 2 DP de ' + str(channel_selected) + ' e: ' + str(mean_channel) + ' +- ' + str(2*std_channel))
# print('A media +- 3 DP de ' + str(channel_selected) + ' e: ' + str(mean_channel) + ' +- ' + str(3*std_channel))

time_datetime = convert_time(data_time)
plot(time_datetime, data, channel_selected, unit)
# outlier, outlier_index = get_outlier(data,data_index)

### Comparacao com outro canal
# channel_comparison = select_channel(channels)
# freq_comparison, time_frame_comparison = get_frequency(reader)
# data_comparison, data_index_comparison, data_time_comparison = interact_channels('get_data', reader, channel_comparison, time_frame_comparison)

# PROXIMOS PASSOS:
# filtrar com base em % da media... 10%? 15%?
# cruzamento com outros canais (no tempo selecionado no canai inicial)
# merge files
# plot "interativo" - pegar valores nos pontos das curvas, clickaveis