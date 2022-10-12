from datetime import datetime

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

#0.00000115741 é o numero magico que acrescenta 100 ms no passo de tempo ----> PARA 10Hz <---
#ele é achado por x = 1/(24*3600*10)
#0.00000003858 é o numero magico que acrescenta 3.33 ms no passo de tempo ----> PARA 300Hz <---
#ele é achado por x = 1/(24*3600*300)
# excel_date = 44769.0 +(0.00000115741)*2 #0.00000115741 é o numero magico que acrescenta 100 ms no passo de tempo

excel_date = 44770.74345145387

dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(excel_date) - 2)
print('dt1: ', dt)
hour, minute, second, millisecond = floatHourToTime(excel_date % 1)
dt = dt.replace(hour=hour, minute=minute, second=second)

print('dt2: ', dt)
print(str(dt), millisecond)
# print(type(str(dt)))

# def convert(tempo_float, tamanho_lista):
#
#     lista_tempo_conv =[]
#     for i in range(tamanho_lista):
#         dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(excel_date) - 2)
#         hour, minute, second, millisecond = floatHourToTime(excel_date % 1)
#         dt = dt.replace(hour=hour, minute=minute, second=second)
#         excel_date = lista[i]
#         lista_tempo_conv.append(dt)