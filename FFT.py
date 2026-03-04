import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# load data
filename = '1902.300000 omega.csv'
# '21877.000000 omega.csv' 双吸引子 '1898.300000 omega.csv' 单吸引子   '1902.300000 omega.csv' 三周期
# '1902.600000 omega.csv' 阵发混沌
# '1903.200000 omega.csv' 四周期    '1903.700000 omega.csv' 双周期   '1904.900000 omega.csv' 单周期
CH2_raw = pd.read_csv(filename,sep=',',header=9,usecols=[0])
CH1_raw = pd.read_csv(filename,sep=',',header=9,usecols=[1])
array1 = CH1_raw.values
array2 = CH2_raw.values
CH1 = []
CH2 = []
for i in range(len(array1)):
    CH1.append(float(array1[i,0]))
    CH2.append(float(array2[i, 0]))
t = np.arange(len(CH1))

# FFT
CH1_fft = np.fft.rfft(CH1)
power1 = [abs(c) for c in CH1_fft]
CH2_fft = np.fft.rfft(CH2)
power2 = [abs(c) for c in CH2_fft]

# plot the power spectrum
loc = t.tolist().index(1000)
plt.plot(t[:loc],power1[:loc])
plt.xlabel('Frequency')
plt.ylabel('Power')
plt.title('U1 Power Spectrum')
plt.show()

'''
plt.plot(t[:loc],power2[:loc])
plt.xlabel('Frequency')
plt.ylabel('Power')
plt.title('U2 Power Spectrum')
plt.show()
'''
