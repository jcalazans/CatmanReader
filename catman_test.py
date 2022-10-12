from apread import APReader
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


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




''' Reading the .bin file '''
reader = APReader(r"C:\Users\jcerqueira\Desktop\ST-21306-10_2_2-Bore_FAT_with_Water_TCN.BIN")


''' dt of a specific channel '''
for channel in reader.Channels:
    #time_test = channel.time
    ch_name = channel.Name
    if ch_name == ('Acceleration_EFA_X'):
        dt = channel.extHeader['dt']              ### dt em milisegundos
        # print('dt: ', dt)
### para pegar o dt em milisegundos a depender da frequencia do canal (em formato float do excel)
if dt == 100:
    passo = 1/(24*3600*10)
if dt == 3.3333333333333335:
    passo = 1/(24*3600*300)




c_name = []                                         ### c_name -> para guardar os nomes dos canais em uma lista
data_time = []                                      ### data_time -> para guardar o tempo dos dados em ms em uma lista
data_index = []                                     ### data_index -> para guardar o indice dos dados em uma lista

''' get info of the groups '''
for group in reader.Groups:
    ### gcname -> posicao na memoria da informacao de TODOS os canais
    gcname = group.Channels
    ### group_Channels -> posicao na memoria da informacao dos canais != de canais de tempo
    group_Channels = group.ChannelsY

    freq = group.frequency                          ### frequencia do canal

    # print('frequencia: ', freq)
    # print(group.interval)
    # print(group.intervalstr)

    ''' get info of the channels '''
    for canais in group_Channels:
        print(canais.Name)                          ### Nome de Todos os Canais
        c_name.append(canais.Name)                  ### c_name -> guarda os nomes dos canais em uma lista (indexando os nomes dos canais)

        ''' manipulating a specific channel'''
        if (canais.Name == 'Acceleration_EFA_X'):
        # if (canais.Name == str(c_name[0])):
            channels_name = canais.Name             ### nome do canal selecionado
            # print('AQUI ',channels_name)
            data_channel = canais.data              ### dados do canal especifico
            mean_v = np.mean(canais.data)           ### media dos dados do canal especifico
            dp_v = np.std(canais.data)              ### desvio padrao dos dados do canal especifico
            max_v = np.max(canais.data)             ### valor maximo dos dados do canal em especifico
            min_v = np.min(canais.data)             ### valor minimo dos dados do canal em especifico
            # print('Especific data (of an especifi channel): ',canais.data[0]) ### primeira entrada de dados do canal (index 0)
            initial_time = canais.extHeader['T0']   ### data/hora (excel) do inicio da aquisicao
            # print('T0: ', initial_time)
            # print('Final time: ', canais.time)    ### tempo final?
            channel_fullName = canais.Time          ### Nome completo do canal de tempo , inclusive com o numero de entradas
            time_length = canais.length             ### numero de entradas de dados/tempo
            # print('tamanho tempo: ', time_length)

            ### criando lista dos tempos em milisegundos (em formato float do excel)
            time = initial_time
            data_time.append(time)
            for n in range(time_length):
                time = time + passo
                data_time.append(time)              ### lista com os tempos pares dos dados do canal especifico
                data_index.append(n)



### transformando em dicionário o canal selecionado
dic_time_data = dict(zip(data_time, data_channel))                              ### dicionario tempo : valor
dic_index_data = dict(zip(data_index, data_channel))                            ### dicionario index : valor
# dic_time_data_2 = {data_time[i]: data_channel[i] for i in range(len(data_time))}### outra maneira de criar o dicionario
max_value = max(dic_index_data.values())                                        ### valor maximo do dicionario
max_key_time = max(dic_time_data, key=dic_time_data.get)                        ### chave do valor maximo do dicionario
max_key_index = max(dic_index_data, key=dic_index_data.get)                     ### chave do valor maximo do dicionario
min_value = min(dic_index_data.values())                                        ### valor minimo do dicionario
min_key_time = min(dic_time_data, key=dic_time_data.get)                        ### chave do valor minimo do dicionario
min_key_index = min(dic_index_data, key=dic_index_data.get)                     ### chave do valor maximo do dicionario

print('valor minimo: ', min_value)
print('chave valor minimo: ', min_key_index)
# print(dic_time_data == dic_time_data_2)
# print('valor da chave (canais de msm freq): ', dic_index_data[36595369])
# print('valor da chave (canal de 300 para 10): ', dic_index_data[round(36595369/30)]) ### divisao por 30 pra ir de chave de indice de canais de 300Hz para 10 Hz
# print('valor da chave (canal de 10 para 300): ', dic_index_data[round(27241*30)])    ### divisao por 30 pra ir de chave de indice de canais de 300Hz para 10 Hz

out_data = []
out_index = []
count = 0
for i in data_channel:
    count += 1
    if (i < (-0.04)) or (i > (0.04)):
        out_data.append(i)
        # print(i)
        out_index.append(count-1)
        # print(out_index)
#
dic_out = dict(zip(out_index, out_data))
# print('dicionario outliers: ', dic_out)
# print(dic_index_data[139537], dic_index_data[139538], dic_index_data[139539])













            ### Converter data float em data compreensivel para plot - A ser melhorado
            # human_eyes =[]
            # for j in range(time_length):
            #     excel_date = data_time[j]
            #     dt_new = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(excel_date) - 2)
            #     hour, minute, second, millisecond = floatHourToTime(excel_date % 1)
            #     dt_new = dt_new.replace(hour=hour, minute=minute, second=second)
            #     human_eyes.append(str(dt_new))

# print(c_name)
            #print(canais.readData())


'''Plot'''
# fig,ax = plt.subplots()
# ax.plot(data_index, data_channel)
# plt.show()

print(dic_out.keys())
print(dic_out.values())

fig,ax = plt.subplots()
ax.plot(out_index, out_data)
plt.show()








    #for ch in gcname:
        #gchname = ch.Name
        #gchdata = ch.data
        #gchtime = ch.time
        #if gchname == ('Axial_Tension_Actuator'):
            #print(gchname)
            #print(gchdata)
            #print(gchtime)
            #x = float(gchtime)
            #for dado in gchdata:
                #print(dado, x)
                #x = x + teste/6000000
            #print(len(gchdata))
    #print(gcname)





"""plot all channels"""
#for channel in reader.Channels:
    #time_test = channel.time
    #cname = channel.Name
    #if cname == ('Axial_Tension_Actuator'):
    #    teste = channel.extHeader['dt']
    #    print(teste)
    #if (time_test == 44770.83899305556) or (time_test == 44770.83902777778):
    #if (cname == "Axial_Tension_Actuator"):
        #print(time_test)
        #print(cname)
















"""========== DOCUMENTATION EXEMPLES ======="""
"""print name of all channels"""
#for channel in reader.Channels:
    #print(channel)         # channel name
"""print  all groups"""
#for group in reader.Groups:
#    print(group)
"""plot all the readers data"""
# reader.plot()
""" plot specific groups"""
#reader.plotGroup(0)           # plot specific group
#reader.plotGroups(0,3)        # group 1 to 3 (1,2,3)
#reader.plot([0, 2, 4])        # group 1, 3 and 5
"""plot specific channels"""
#group.plotChannel(4)            # plot specific Channel
#group.plotChannels(0,2)        # plot range of Channels
# group.plot([3])              # print channels 2 and 4
"""========== END OF DOCUMENTATION EXEMPLES ======="""