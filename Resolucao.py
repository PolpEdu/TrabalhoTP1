import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.io import wavfile
import math
from huffmancodec import *
import time
import sklearn.metrics as s


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


def lerficheiro(nome):
    ext = nome.split(".")[1]
    PATH = "./data/" + nome

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

    return alfabeto, data


def entropia(ocorrencias, alfab):
    H = 0
    somatotal = 0
    ptotal = 0
    # print(ocorrencias)
    for x in ocorrencias:
        somatotal += x

    for k in range(len(alfab)):
        p = ocorrencias[k] / somatotal
        if p == 0:  # o elemento do alfabeto não existe na fonte de informação
            continue
        ptotal += p

        i = math.log2(1 / p)
        H += i * p

    print(f"O limite mínimo teórico para o número"
          f" médio de bits por símbolo da fonte dada é:\n{H:.5f} bits/simbolo")
    return H


def huffmancodec(data):
    codec = HuffmanCodec.from_data(data)
    symbols, lenghts = codec.get_code_len()

    # print(symbols)
    # print(lenghts)
    return symbols, lenghts


def agrupar(data):
    if len(data) % 2 == 1:
        data = data[:-1]  # tiro o ultimo elemento

    novafonte = [[0 for y in range(2)] for x in range(int(len(data) / 2))] #agrupar por indice par e indice impar
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

    #print(f"Data agrupada:{novafonte}")
    return novafonte


def entropiaHuffman(length, symbols, ocorrencias):
    numerador = 0
    denominador = 0

    for x in range(len(symbols)):
        numerador += length[x] * ocorrencias[x]

    """
    print("s:" + str(symbols))
    print("l:" + str(length))
    print("o:" + str(ocorrencias))
    """

    for x in range(len(length)):
        denominador += ocorrencias[x]

    H = numerador / denominador

    print(f"O limite mínimo teórico para o número"
          f" médio de bits por símbolo da fonte dada codificada em Huffman é:\n{H:.5f} bits/simbolo")


def InfMut(query,target,alfabeto,passo):
    infmutua = []
    sublista = []
    p = 0

    while p < len(target) - len(query)+1:
        for x in target[p:p + len(query)]:
            sublista.append(x)

        print(sublista, query)
        #TODO: como meter isto a funcionar (esta a dar mal agora)
        infmut = s.mutual_info_score(query,sublista) #TODO: perguntar ao stor se é na boa calcular a informação mutua
        infmutua.append(infmut)
        p += passo
        sublista = []

    return infmutua

def main():
    [alfabeto, data] = lerficheiro("english.txt")

    ocorrencias = [data.count(i) for i in alfabeto]

    # entropia normal:
    H1 = entropia(ocorrencias, alfabeto)
    print(f"O limite mínimo teórico para o número"
          f" médio de bits por símbolo da fonte dada é:\n{H1:.5f} bits/simbolo")
    criarhist(ocorrencias, alfabeto)


    # ex 4
    symbols, length = huffmancodec(data)
    H2= entropiaHuffman(length, symbols,ocorrencias)  # entropia codificação de huffman = entropia normal + 1. No pior dos casos.

    # ex 5
    print("\nAgrupando a data...")
    dataagrupada = agrupar(data)

    alfabetoagrupado = []
    for x in dataagrupada:
        if x not in alfabetoagrupado:
            alfabetoagrupado.append(x)

    ocodataagrupada = [dataagrupada.count(i) for i in alfabetoagrupado]

    print(ocodataagrupada)

    # print("alfabeto agrupado:"+str(alfabetoagrupado))
    h = entropia(ocodataagrupada, alfabetoagrupado)
    #como temos dois simbolos por elemento do alfabeto se quiser o limite de bits por simbolo tenho que dividir por 2.
    h = h/2
    print(f"O limite mínimo teórico para o número"
          f" médio de bits por símbolo da fonte dada é:\n{h:.5f} bits/simbolo")

    # ex 6
    # I(X,Y) - Informação mutua.
    query = [2, 6, 4, 10, 5, 9, 5, 8, 0, 8];
    target = [6, 8, 9,7, 2, 4, 9, 9, 4, 9, 1, 4, 8, 0, 1, 2, 2, 6, 3, 2, 0, 7, 4, 9, 5, 4,8, 5, 2, 7, 8, 0, 7, 4, 8, 5, 7, 4, 3, 2, 2, 7, 3, 5, 2, 7, 4, 9, 9, 6];
    alfabeto = [0, 1, 2, 3,4,5,6,7,8,9, 10];
    passo = 1

    infm = InfMut(query,target,alfabeto,passo)
    print(f"{infm}")



if __name__ == "__main__":
    main()

# O limite mínimo teórico para o número médio de bits por símbolo da fonte dada é:
# 3.46587 bits/simbolo - homer.bmp valor normal
# O limite mínimo teórico para o número médio de bits por símbolo da fonte dada codificada em Huffman é:
# 3.54832 bits/simbolo - homer.bmp codificação huffman valor correto
# 2.41273 bits/simbolo
