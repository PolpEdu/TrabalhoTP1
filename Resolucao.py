import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.io import wavfile
import math
from huffmancodec import *
import time

data = np.random.randint(0, 10, size=20)


def criarhist(ocorrencias, alfabeto):
    # print(ocorrencias)
    # ppapra aparecer todos:
    # plt.xticks(range(len(ocorrencias)), alfabeto)

    wh = (14, 8)
    plt.figure(figsize=wh)
    plt.bar(alfabeto, ocorrencias, ec="k")

    plt.xlabel('Alfabeto', fontsize=15)
    plt.ylabel('Ocorrencias', fontsize=15)
    plt.show()


def lerwavCanalDireito(nome):
    ext = nome.split(".")[1]
    PATH = "./data/" + nome
    if ext == "wav":
        print("Lendo " + nome)
        [fs, info] = wavfile.read(PATH)
        max = math.pow(2, int(str(info.dtype).split("int")[1]))
        alfabeto = [x for x in range(0, int(max + 1))]
        d = [fs, info]
        # print(d[1])
        data = list(d[1])

    # print(f"Data:{data}")

    return alfabeto, data


def lerficheiro(nome):
    ext = nome.split(".")[1]
    PATH = "./data/" + nome
    print("Lendo " + nome)
    if ext == "txt":
        # Caracteres ASCII, existe 127 caracteres ASCII
        alfabeto = [x for x in range(48, 123)]

        # nao devem entrar
        # tirar todos os simbolos.
        for i in range(58, 65):
            alfabeto.remove(i)
        for i in range(91, 97):
            alfabeto.remove(i)  # tirar o espaço. ascii = 32

        with open(PATH, "r", encoding='ASCII') as f:
            rd = f.read()
            f.close()

        data = [ord(char) for char in rd]

    elif ext == "bmp":
        # bmp os valores usados (preto a branco) vão de 0 a 255
        alfabeto = [x for x in range(0, 255 + 1)]
        datasquare = mpimg.imread(PATH)
        d = datasquare.flatten()
        # print(type(d))
        data = list(d)

    elif ext == "wav":

        [fs, info] = wavfile.read(PATH)

        # como o dtype é sempre int*BITS*
        # vou e tiro o numero de bits por cada amostra para conseguir o maior valor
        # print(str(info.dtype).split("int")[1])
        max = math.pow(2, int(str(info.dtype).split("int")[1]))

        # Wav normalizado vai de 0 a max+1.
        alfabeto = [x for x in range(0, int(max + 1))]

        d = [fs, info]

        data = list(d[1])
        # print(type(data))

    # print(f"Alfabeto:{alfabeto}\n"f"Data:{data}")
    print("Saved!")
    return alfabeto, data


def entropia(ocorrencias):
    ocorrencias = np.array(ocorrencias)
    p = ocorrencias[ocorrencias > 0] / np.sum(ocorrencias)
    H = np.sum(p * np.log2(1 / p))
    # print(f"O limite mínimo teórico para o número"
    #      f" médio de bits por símbolo da fonte dada é:\n{H:.5f} bits/simbolo")
    return H


def compressao_max(alfabeto, entropia):
    Hmax = np.log2(len(alfabeto))
    return ((Hmax - entropia) / Hmax) * 100


def huffmancodec(data):
    codec = HuffmanCodec.from_data(data)
    symbols, lenghts = codec.get_code_len()

    # print(len(symbols))
    # print(len(lenghts))
    return symbols, lenghts


def agrupar(data):
    if len(data) % 2 == 1:
        data = data[:-1]  # tiro o ultimo elemento

    novafonte = [[0 for y in range(2)] for x in range(int(len(data) / 2))]  # agrupar por indice par e indice impar
    i = 0
    j = 0

    for x in range(int(len(data))):
        if x % 2 == 0:

            novafonte[i][j] = data[x]
            j += 1

        else:
            novafonte[i][j] = data[x]
            j = 0
            i += 1

    # print(f"Data agrupada:{novafonte}")
    return novafonte


def entropiaHuffman(length, symbols, ocorrencias, alfabeto):
    numerador = 0
    numerador2 = 0
    denominador = 0

    # print(alfabeto)
    # print(length, len(length))
    # print(symbols, len(symbols))
    # print(ocorrencias, len(ocorrencias))

    # ordenar as ocorrencias
    novasocoreencias = [0] * len(symbols)  # criar uma lista com o mesmo tamanho das ocorrencias
    i = 0

    #contar as ocorrencias de cada simbolo na fonte
    for x in range(len(alfabeto)):
        if i != len(symbols): # para não dar overflow
            if alfabeto[x] == symbols[i]: # se os simbolos tiverem o alfabeto
                novasocoreencias[i] = ocorrencias[x] #adiciono a ocorrencia
                i += 1

    # print(novasocoreencias)



    for x in range(len(symbols)):
        numerador += length[x] * novasocoreencias[x] # contagens da media normal
        numerador2 += math.pow(length[x], 2) * novasocoreencias[x] # vai servir para a varianca



    for x in range(len(novasocoreencias)):
        denominador += novasocoreencias[x] #somar todas as ocorrencias

    E = numerador / denominador  # E(X)^2
    E2 = numerador2 / denominador  # E(X^2)
    V = E2 - math.pow(E, 2)  # formula da varianca: V(x) = E(X^2) - E(X)^2

    print(f"O limite mínimo teórico para o número"
          f" médio de bits por símbolo da fonte dada codificada em Huffman é:\n{E:.5f} bits/simbolo\n E a variancia é"
          f" dada por: {V:.5f}")


def calcinfmut(query, sublista, ocoquery):
    dictocosublista = {}
    for x in sublista: # para cada valor na sublista
        x = str(x)
        if x not in dictocosublista.keys():
            dictocosublista[x] = 1
        else:
            dictocosublista[x] += 1 # valor ja existe no dicionario, adiciona 1

    ocosublista = list(dictocosublista.values()) # passa os valores do dicionario para uma lista

    listaintersecao = []
    for x in range(len(query)):
        listaintersecao.append([query[x], sublista[x]]) #lista de interseção das duas listas

    dictoco = {}
    for x in listaintersecao:  # para cada valor na lista da interseção
        x = str(x)
        # contar as suas ocorrencias
        if x not in dictoco.keys():
            dictoco[x] = 1  # chave ainda não está no dicionario
        else:
            dictoco[x] += 1  # chave no dicionario, adicionar 1 à ocorrencia.

    listaoco = list(dictoco.values())# passar para lista todos os objetos do dicionario.

    # print(dictoco)

    # print(listacombosalf)
    # print(listaintersecao)
    # print(listaoco)

    # print("listaoco :" + str(listaoco))
    # print("listaintersecao :" + str(listaintersecao))
    # print("listacombosalf len:" + str(listacombosalf))
    # print("lista query len:" + str(len(query)))

    # preciso de passar o tamanho da lista de intersecao para calcular a entropia
    h1h2 = entropiaIntersecao(listaoco, len(listaintersecao))
    h1 = entropia(ocoquery)
    h2 = entropia(ocosublista)

    infmut = h1 + h2 - h1h2
    return infmut


def entropiaIntersecao(listaoco, lenlistaintersecao):
    ocorrencias = np.array(listaoco)
    p = ocorrencias[ocorrencias > 0] / lenlistaintersecao
    H = -np.sum(p * np.log2(p))
    return H


def InfMut(query, target, passo):
    infmutua = []
    sublista = []
    p = 0
    print("Calculando a informação mutua...")
    while p < len(target) - len(query) + 1:
        for x in target[p:p + len(query)]:
            sublista.append(x)


        dictocoquery = {}
        for x in query:  # para cada valor na query
            x = str(x)
            if x not in dictocoquery.keys():  # anota a sua ocorrencia no dicionario
                dictocoquery[x] = 1
            else:
                dictocoquery[x] += 1  # valor ja existe no dicionario, adiciona 1
        ocoquery = list(dictocoquery.values())  # passa os valores do dicionario para uma lista


        infmut = calcinfmut(query, sublista, ocoquery)
        infmut = round(infmut, 4)
        infmutua.append(infmut)
        p += passo
        sublista = []

    print("Calculado! - ", str(infmutua))
    plt.plot(infmutua)  # para fazer o plot das respetivas informações mutuas ao longo do tempo.
    plt.show()  # mostrar o plot.
    print("Sorting....")
    infmutua.sort()  # atenção! Está sorted! não vai bater com a solução escrita exatamente no papel
    infmutua.reverse()  # para ficar decrescente
    return infmutua


def main():
    [alfabeto, dataA] = lerficheiro("english.txt")

    # limpar a data com o nosso alfabeto
    data = []
    for x in dataA:
        if x in alfabeto:
            data.append(x)

    ocorrencias = [data.count(i) for i in alfabeto]

    # entropia normal:
    H1 = entropia(ocorrencias)  # ex 2
    CompMax = compressao_max(alfabeto, H1)
    print(f"O limite mínimo teórico para o número"
          f" médio de bits por símbolo da fonte dada é:\n{H1:.5f} bits/simbolo")
    print(f"Compressão máxima da fonte dada:\n{CompMax:.2f} %")
    #criarhist(ocorrencias, alfabeto)  # ex 1

    # ex 4
    symbols, length = huffmancodec(data)
    # print("Hffman")
    # print(symbols)
    # print(length)
    H2 = entropiaHuffman(length, symbols, ocorrencias,
                         alfabeto)  # entropia codificação de huffman = entropia normal + 1. No pior dos casos.


    # ex 5
    print("\nAgrupando a data...")
    dataagrupada = agrupar(data)

    alfabetoagrupado = []
    for x in dataagrupada:
        if x not in alfabetoagrupado:
            alfabetoagrupado.append(x)

    ocodataagrupada = [dataagrupada.count(i) for i in alfabetoagrupado]

    # print(ocodataagrupada)

    # print("alfabeto agrupado:"+str(alfabetoagrupado))
    h = entropia(ocodataagrupada)
    # como temos dois simbolos por elemento do alfabeto se quiser o limite de bits por simbolo tenho que dividir por 2.
    h = h / 2
    print(f"O limite mínimo teórico para o número"
          f" médio de bits por símbolo da fonte dada é:\n{h:.5f} bits/simbolo")

    #criarhist(ocodataagrupada, alfabeto)

    # ex 6:
    # I(X,Y) - Informação mutua.
    '''
    Para teste:
    '''

    query = [2, 6, 4, 10, 5, 9, 5, 8, 0, 8]
    target = [6, 8, 9, 7, 2, 4, 9, 9, 4, 9, 1, 4, 8, 0, 1, 2, 2, 6, 3, 2, 0, 7, 4, 9, 5, 4, 8, 5, 2, 7, 8, 0, 7, 4, 8,
              5, 7, 4, 3, 2, 2, 7, 3, 5, 2, 7, 4, 9, 9, 6]
    alfabeto = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    passo = 1

    infm = InfMut(query, target, passo)
    print(f"InfoMutua entre \"query\" e \"target\" ={infm}")

    # 6 b)
    [alfabeto, query] = lerficheiro("guitarSolo.wav")
    [alfabeto1, target1] = lerficheiro("target01 - repeat.wav")
    [alfabeto2, target2] = lerficheiro("target02 - repeatNoise.wav")
    passo = round(len(query) / 4)

    if alfabeto != alfabeto1 or alfabeto != alfabeto2:
        print("Os alfabetos do query e target não coincidem. Não é possivel calcular a informação mútua entre eles.")
        quit(1)

    infm = InfMut(query, target1, passo)
    print(f"InfoMutua entre \"guitarSolo.wav\" e \"target01 - repeat.wav\" ={infm}")
    infm2 = InfMut(query, target2, passo)
    print(f"InfoMutua entre \"guitarSolo.wav\" e \"target02 - repeatNoise.wav\" ={infm2}")

    # 6 c)
    print("Calcular o conjunto de todas as informações mútuas:")
    infmutuas = informacoesmutuas(query, alfabeto)

    for k, v in infmutuas.items():
        print("Informações mútuas ordenadas por ordem decrescente do wav \"" + str(k) + "\":")
        print(v)

    infmax(infmutuas)  # função que dá print às informações mutuas máximas em cada ficheiro wav.


def informacoesmutuas(query, alfabeto):
    infsMuts = {}
    passo = round(len(query) / 4)

    for x in range(1, 8):
        name = "Song0" + str(x) + ".wav"
        [alf, targ] = lerficheiro(name)
        if alf != alfabeto:
            print("Os alfabetos do query e target não coincidem.")
            quit(1)
        infmut = InfMut(query, targ, passo)

        infsMuts[name] = infmut
    return infsMuts


def infmax(dictinfmuts):
    for k, v in dictinfmuts.items():
        print("Informação mútua máxima no wav \"" + str(k) + "\" corresponde a " + str(v[0]))


if __name__ == "__main__":
    main()

# O limite mínimo teórico para o número médio de bits por símbolo da fonte dada é:
# 3.46587 bits/simbolo - homer.bmp valor normal
# O limite mínimo teórico para o número médio de bits por símbolo da fonte dada codificada em Huffman é:
# 3.54832 bits/simbolo - homer.bmp codificação huffman valor correto
# 2.41273 bits/simbolo
