import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.io import wavfile
import math
from huffmancodec import *
import time

data = np.random.randint(0, 10, size=20)


def criarhist(data, alfabeto):
    ocorrencias = [data.count(i) for i in alfabeto]
    # print(ocorrencias)

    # ppapra aparecer todos:
    # plt.xticks(range(len(ocorrencias)), alfabeto)

    wh = (14, 8)
    plt.figure(figsize=wh)
    plt.bar(alfabeto, ocorrencias, ec="k")

    plt.xlabel('Alfabeto', fontsize=15)
    plt.ylabel('Ocorrencias', fontsize=15)
    plt.show()


def limitebits(data, alfab):
    H = 0
    for k in alfab:
        p = list(data).count(k) / len(data)
        if p == 0:  # o elemento do alfabeto não existe na fonte de informação
            continue
        i = math.log2(1 / p)
        H += i * p

    print(f"O limite mínimo teórico para o número"
          f" médio de bits por símbolo da fonte dada é:\n{H:.5f} bits/simbolo")
    return H


def lerficheiro(nome):
    ext = nome.split(".")[1]
    PATH = "./data/" + nome

    if ext == "txt":
        # Caracteres ASCII, existe 127 caracteres ASCII
        alfabeto = [x for x in range(0, 127 + 1)]

        # TODO: espaços contam?
        alfabeto.remove(32)  # tirar o espaço. ascii = 32
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

    print(f"Alfabeto:{alfabeto}\n"
          f"Data:{data}")

    return alfabeto, data


def entropia(data, alfab):
    H = 0
    for k in alfab:
        p = list(data).count(k) / len(data)
        if p == 0:  # o elemento do alfabeto não existe na fonte de informação
            continue
        i = math.log2(1 / p)
        H += i * p

    print(f"O limite mínimo teórico para o número"
          f" médio de bits por símbolo da fonte dada é:\n{H:.5f} bits/simbolo")
    return H


def nrmediobits(data):
    codec = HuffmanCodec.from_data(data)
    symbols, lenghts = codec.get_code_len()
    print(symbols)
    # print(lenghts)
    return symbols, lenghts


def agrupar(data):
    if len(data) % 2 == 1:
        data = data[:-1]  # tiro o ultimo elemento
    
    novafonte = [[0 for y in range(2)] for x in range(int(len(data) / 2))]
    
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

    print(f"{novafonte}")
    return novafonte


if __name__ == "__main__":
    [alfabeto, data] = lerficheiro("english.txt")
    entropia(data, alfabeto)
    criarhist(data, alfabeto)

    # ex 4

    symbols, lenght = nrmediobits(data)
    print("Usando a codificação de Huffman...")
    entropia(symbols, alfabeto)  # TODO: esta bem? ver se dá valores aceitaveis.

    # ex 5
    dataagrupada = agrupar(data) # TODO: esta mal provavelmente
    entropia(dataagrupada, alfabeto)
