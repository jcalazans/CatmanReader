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

c_name = []                                         ### c_name -> para guardar os nomes dos canais em uma lista
data_time = []

''' get info of the groups '''
for group in reader.Groups:
    ### gcname -> posicao na memoria da informacao de TODOS os canais
    group_Channels_Time = group.Channels
    ### group_Channels -> posicao na memoria da informacao dos canais != de canais de tempo
    group_Channels = group.ChannelsY

    freq = group.frequency                          ### frequencia do canal
    # print('frequencia: ', freq)
    # print(group.interval)
    # print(group.intervalstr)

    ''' get info of the channels '''
    # for canais in group_Channels_Time:              ### considerando os canais de tempo tambem
    for canais in group_Channels:                   ### considerando os canais != de canais de tempo
        print(canais.Name)                          ### Nome de Todos os Canais
        c_name.append(canais.Name)                  ### c_name -> guarda os nomes dos canais em uma lista (indexando os nomes dos canais)

channel_selected = int(input('Qual a posicao do canal desejado? (sendo a primeria posicao = 1)'))


####------------------------------------------------------------------------

### ESTA SELECIONANDO CERTO
### PROXIMO PASSO: COMO USAR O INDEX DO INPUT PARA DAR SEGUIMENTO
### OU SEJA, "PUXAR" dt -> OK

####-------------------------------------------------------------------------




ch_name_list = []

''' dt of a specific channel '''
for channel in reader.Channels:
    ch_name = channel.Name
    ch_name_list.append(ch_name)

for i in range(len(ch_name_list)):
    if ch_name_list[i] == (str(c_name[channel_selected-1])):
        print(c_name[channel_selected-1])
        dt = channel.extHeader['dt']              ### dt em milisegundos
        # print('dt: ', dt)

if dt == 3.3333333333333335:
    passo = 1/(24*3600*(10))
# if dt == 300: ### consertar esse dt
#     passo = 1/(24*3600*dt)



####------------------------------------------------------------------------
### OK ATE AQUI - ja estou conseguindo selecionar o canal
####------------------------------------------------------------------------


# Como fazer para pegar os dados do canal em especifico, selecionado anterioremente
# considerando o input dado????


# print(ch_name)

c_name = []                                         ### c_name -> para guardar os nomes dos canais em uma lista
# data_time = []

# print(ch_name_list)

''' get info of the groups '''
for group in reader.Groups:
    ### gcname -> posicao na memoria da informacao de TODOS os canais
    gcname = group.Channels
    # ### group_Channels -> posicao na memoria da informacao dos canais != de canais de tempo
    group_Channels = group.ChannelsY

    # freq = group.frequency                          ### frequencia do canal

    # print('frequencia: ', freq)
    # print(group.interval)
    # print(group.intervalstr)



    ''' get info of the channels '''
    for canais in group_Channels:
        # print('CANAIS NAME', canais.Name)                          ### Nome de Todos os Canais
        c_name.append(canais.Name)                  ### c_name -> guarda os nomes dos canais em uma lista (indexando os nomes dos canais)
        print(len(ch_name_list))
        # for i in range(len(c_name)):
        #
        #     print(str(c_name))

        ''' manipulating a specific channel'''
        if (c_name[i] == str(c_name[channel_selected-1])):
            print(str(c_name[i]))
            print(str(c_name[channel_selected-1]))
            print(c_name[i] == str(c_name[channel_selected-1]))
            channels_name = canais.Name             ### nome do canal selecionado
            data_channel = canais.data              ### dados do canal especifico
            mean = np.mean(canais.data)             ### media dos dados do canal especifico
            dp = np.std(canais.data)                ### desvio padrao dos dados do canal especifico
            max = np.max(canais.data)               ### valor maximo dos dados do canal em especifico
            min = np.min(canais.data)               ### valor minimo dos dados do canal em especifico
            # print('Especific data (of an especifi channel): ',canais.data[0]) ### primeira entrada de dados do canal (index 0)
            initial_time = canais.extHeader['T0']   ### data/hora (excel) do inicio da aquisicao
            # print('Final time: ', canais.time)    ### tempo final?
            channel_fullName = canais.Time          ### Nome completo do canal de tempo , inclusive com o numero de entradas
            time_length = canais.length             ### numero de entradas de dados/tempo

            ### criando lista dos tempos
            time = initial_time
            for n in range(time_length):
                time = time + passo
                data_time.append(time)              ### lista com os tempos pares dos dados do canal especifico

        # print(data_channel)

print('SAIU')
print(len(data_channel))
print(len(data_time))

            ### Converter data float em data compreensivel para plot - A ser melhorado
            # human_eyes =[]
            # for j in range(time_length):
            #     excel_date = data_time[j]
            #     dt_new = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(excel_date) - 2)
            #     hour, minute, second, millisecond = floatHourToTime(excel_date % 1)
            #     dt_new = dt_new.replace(hour=hour, minute=minute, second=second)
            #     human_eyes.append(str(dt_new))





#### CRIAR DICIONARIO CHAVE:VALOR DOS DADOS DESEJADOS E TEMPO,
### PARA CONSEGUIR COLETAR UM TEMPO ESPECÍFICO DADO UM VALOR SELEICONADO (POR EXEMPLO, VALOR MINIMO)

# print(c_name)




'''Plot'''
# fig,ax = plt.subplots()
# ax.plot(data_time, data_channel)
# plt.show()








### ========================================================================
# print(canais.readData())
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