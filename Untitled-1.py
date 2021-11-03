import random
import math


def sumImaginaryNumbers():
    a = 1+2j
    b = 3+4j
    c = a+b
    print(c)


def main():
    # Para teste:
    query = [2, 6, 4, 10, 5, 9, 5, 8, 0, 8]
    target = [6, 8, 9, 7, 2, 4, 9, 9, 4, 9, 1, 4, 8, 0, 1, 2, 2, 6, 3, 2, 0, 7, 4, 9, 5, 4, 8, 5, 2, 7, 8, 0, 7, 4, 8,
              5, 7, 4, 3, 2, 2, 7, 3, 5, 2, 7, 4, 9, 9, 6]
    alfabeto = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    passo = 1

    # [queryalfabeto, query] = lerficheiro("guitarsolo.wav")
    # passo = len(query) / 4

    # [alfabeto, data] = lerficheiro("english.txt")

    infm = InfMut(query, target, alfabeto, passo)
    print(f"InfoMutua ={infm}")


def InfMut(query, target, alfabeto, passo):
    infmutua = []
    sublista = []
    p = 0

    while p < len(target) - len(query) + 1:
        for x in target[p:p + len(query)]:
            sublista.append(x)

        print("\n" + str(sublista) + "\n" + str(query))

        # tenho que dividir por log(2) para me dar o numero por bits.
        infmut = mutualInformation(query, sublista)

        infmut = round(infmut, 4)
        infmutua.append(infmut)
        p += passo
        sublista = []

    return infmutua

# calculate the entropy of a list using numpy


def entropy(list):
    # calculate the entropy
    return -sum([(item[1] * math.log(item[1], 2)) for item in list])

# calculate the joint probability of two lists


def jointprobability(list1, list2):
    # initialize the joint probability
    jointProbability = {}

    # calculate the joint probability
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                if item1 in jointProbability:
                    jointProbability[item1] += 1
                else:
                    jointProbability[item1] = 1

    # convert to a list of tuples
    jointProbability = list(jointProbability.items())

    newjoint = []
    for x in jointProbability:
        x = list(x)
        newjoint.append(x)

    print(newjoint)

    # convert to a list of frequencies
    for item in newjoint:
        item[1] = item[1] / (len(list1) * len(list2))

    return newjoint


def marginalProbability(lista, jointProbability):
    # initialize the marginal probability
    marginalProbability = {}

    # calculate the marginal probability
    for item in lista:
        if item in marginalProbability:
            marginalProbability[item] += 1
        else:
            marginalProbability[item] = 1

    # convert to a list of tuples
    marginalProbability = list(marginalProbability.items())

    # passar para lista de listas.
    newmarginalProbability = []
    for x in marginalProbability:
        x = list(x)
        newmarginalProbability.append(x)

    print(newmarginalProbability)

    # convert to a list of frequencies
    for item in newmarginalProbability:
        item[1] = item[1] / len(lista)

    return newmarginalProbability


def mutualInformation(list1, list2):
    # calculate the joint probability
    jointProbability = jointprobability(list1, list2)

    # calculate the marginal probability of the first list
    marginalProbability1 = marginalProbability(list1, jointProbability)

    # calculate the marginal probability of the second list
    marginalProbability2 = marginalProbability(list2, jointProbability)

    # calculate the mutual information
    return entropy(marginalProbability1) + entropy(marginalProbability2) - entropy(jointProbability)


# This is the standard boilerplate that calls the main() function.
main()
