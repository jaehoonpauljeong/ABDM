from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

x = [100000, 200000, 300000, 400000, 500000, 600000, 700000]
algorithms = ['plaintext', 'des', '3des', 'aes', 'abdm']
for algorithm in algorithms:
    y = []
    for data_num in x:
        df = pd.read_csv('results/{0}/{0}_data_num_{1}_insert.csv'.format(algorithm, str(data_num)))
        y.append(df['insert-time'].mean())
    if algorithm == 'plaintext':
        plt.plot(x, y, 'blue', linestyle='solid', marker='s', label='Plain Text')
    elif algorithm == 'des':
        plt.plot(x, y, 'orange', linestyle='dashed', marker='o', label='DES')
    elif algorithm == '3des':
        plt.plot(x, y, 'green', linestyle='dotted', marker='+', label='3DES')
    elif algorithm == 'aes':
        plt.plot(x, y, 'red', linestyle='dotted', marker='d', label='AES256')
    elif algorithm == 'abdm':
        plt.plot(x, y, 'violet', linestyle='dashed', marker='h', label='ABDM')

plt.xlabel('The Amount of Data')
plt.ylabel('Storage Time [sec]')
plt.legend(loc='upper right')
plt.savefig('results/figures/figure5a.eps', format='eps')
plt.show()

for algorithm in algorithms:
    y = []
    for data_num in x:
        df = pd.read_csv('results/{0}/{0}_data_num_{1}_select.csv'.format(algorithm, str(data_num)))
        y.append(df['select-time'].mean())
    if algorithm == 'plaintext':
        plt.plot(x, y, 'blue', linestyle='solid', marker='s', label='Plain Text')
    elif algorithm == 'des':
        plt.plot(x, y, 'orange', linestyle='dashed', marker='o', label='DES')
    elif algorithm == '3des':
        plt.plot(x, y, 'green', linestyle='dotted', marker='+', label='3DES')
    elif algorithm == 'aes':
        plt.plot(x, y, 'red', linestyle='dotted', marker='d', label='AES256')
    elif algorithm == 'abdm':
        plt.plot(x, y, 'violet', linestyle='dashed', marker='h', label='ABDM')

plt.xlabel('The Amount of Data')
plt.ylabel('Retrieval Time [sec]')
plt.legend(loc='upper right')
plt.savefig('results/figures/figure5b.eps', format='eps')
plt.show()



for algorithm in algorithms:
    y = []
    for data_num in x:
        df = pd.read_csv('results/{0}/{0}_data_num_{1}_insert.csv'.format(algorithm, str(data_num)))
        y.append(df['insert-memory'].mean())
    if algorithm == 'plaintext':
        plt.plot(x, y, 'blue', linestyle='solid', marker='s', label='Plain Text')
    elif algorithm == 'des':
        plt.plot(x, y, 'orange', linestyle='dashed', marker='o', label='DES')
    elif algorithm == '3des':
        plt.plot(x, y, 'green', linestyle='dotted', marker='+', label='3DES')
    elif algorithm == 'aes':
        plt.plot(x, y, 'red', linestyle='dotted', marker='d', label='AES256')
    elif algorithm == 'abdm':
        plt.plot(x, y, 'violet', linestyle='dashed', marker='h', label='ABDM')

plt.xlabel('The Amount of Data')
plt.ylabel('Memory Usage [MB]')
plt.legend(loc='upper right')
plt.savefig('results/figures/figure5c.eps', format='eps')
plt.show()

for algorithm in algorithms:
    y = []
    for data_num in x:
        df = pd.read_csv('results/{0}/{0}_data_num_{1}_select.csv'.format(algorithm, str(data_num)))
        y.append(df['select-memory'].mean())
    if algorithm == 'plaintext':
        plt.plot(x, y, 'blue', linestyle='solid', marker='s', label='Plain Text')
    elif algorithm == 'des':
        plt.plot(x, y, 'orange', linestyle='dashed', marker='o', label='DES')
    elif algorithm == '3des':
        plt.plot(x, y, 'green', linestyle='dotted', marker='+', label='3DES')
    elif algorithm == 'aes':
        plt.plot(x, y, 'red', linestyle='dotted', marker='d', label='AES256')
    elif algorithm == 'abdm':
        plt.plot(x, y, 'violet', linestyle='dashed', marker='h', label='ABDM')

plt.xlabel('The Amount of Data')
plt.ylabel('Memory Usage [MB]')
plt.legend(loc='upper right')
plt.savefig('results/figures/figure5d.eps', format='eps')
plt.show()


