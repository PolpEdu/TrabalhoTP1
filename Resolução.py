import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.io import wavfile
import math
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
        with open(PATH, "r", encoding='ASCII') as f:
            rd = f.read()
            f.close()

        #espaços contam?
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


if __name__ == "__main__":
    [alfabeto, data] = lerficheiro("english.txt")
    entropia(data, alfabeto)
    criarhist(data, alfabeto)
