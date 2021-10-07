import matplotlib.pyplot as plt

P = [1, 2, 3, 4, 5, 6, 2, 3, 5, 2, 2, 4, 6]

ola = "123"
def histograma(data):
    plt.hist(data)
    plt.show()


histograma(P)
