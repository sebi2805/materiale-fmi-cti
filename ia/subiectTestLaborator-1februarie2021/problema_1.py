import numpy as np
import matplotlib.pyplot as plt


#incarca exemplele cu litera a (a mic) si A (A mare)
exemple_a_mic = np.loadtxt("data/a_small.txt")
print(exemple_a_mic.shape)
exemple_A_mare = np.loadtxt("data/A_big.txt")
print(exemple_A_mare.shape)

#ploteaza 
litere = ['a', 'A']
nr_exemple_litere = 5
plt.figure
for i in range(len(litere)):
    if(litere[i] == "a"):
        exemple = exemple_a_mic
    if(litere[i] == "A"):
        exemple = exemple_A_mare
    for j in range(nr_exemple_litere):
        plt.subplot(len(litere), nr_exemple_litere, i*nr_exemple_litere+j+1)
        litera = np.uint8(np.transpose(np.reshape(exemple[j,:],(28,28))))
        plt.axis('off')
        plt.imshow(litera,cmap = "gray")
