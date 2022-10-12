from apread import APReader
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

input_file = "C:\\Users\\jcerqueira\\Desktop\\ST-21306-10_2_2-Bore_FAT_with_Water_TCN.BIN"

'''Function convert time float to time human eye'''
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

def app_read(input_file):
    reader = APReader(r'' + input_file + '')
    return reader

def interact_channels(function, reader, channel_selected='null'):
    cname = []
    for group in reader.Groups:
        group_channels = group.ChannelsY
        for channel in group_channels:
            cname.append(channel.Name)
            if (channel.Name == channel_selected) and (channel.Name != 'null'):
                data = channel.data
                data_length = channel.length
    if function == 'read_channels':
        return cname
    elif function == 'get_data':
        return data, data_length

def select_channel(channels):
    for coption in channels:
        index = channels.index(coption)
        print(str(index) + ' - ' + coption)
    channel_selected = int(input('Selecione o numero do Canal Desejado:'))
    cname = channels[channel_selected]
    return cname

reader = app_read(input_file)
channels = interact_channels('read_channels', reader)
channel_selected = select_channel(channels)
data, data_length = interact_channels('get_data', reader, channel_selected)

# PROXIMOS PASSOS:
# descobrir a frequencia do canal selecionado
# medidas estatisticas
# outliers
# cruzamento com outros canais (no tempo selecionado no canai inicial)
# plot