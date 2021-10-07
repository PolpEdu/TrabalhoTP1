import numpy as np
import matplotlib.pyplot as plt

alfabeto = {}

def cria_alfabeto(alfabeto):
    for i in range(ord('A') , ord('Z')+1):
        alfabeto[i] = 0
    for i in range(ord('a') , ord('z')+1):
        alfabeto[i] = 0



def ocorrencias(alfabeto , string):
    for i in range(len(string)):
        for k in range(ord('A') , ord('Z')+1):
            if(string[i] == chr(k)):
                alfabeto[k] += 1
        for j in range(ord('a') , ord('z')+1):
            if(string[i] == chr(j)):
                alfabeto[j] += 1

            
                

cria_alfabeto(alfabeto)
string = "12331sdasdasd"
ocorrencias(alfabeto,string)
max_value = max(alfabeto.values())
print(alfabeto)
plt.ylim([0,max_value])
plt.plot( list(alfabeto) , list(alfabeto.values())  , "r") 
