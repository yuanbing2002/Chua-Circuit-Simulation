import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# load data
filename = '20000101_022739s.csv'
# '20000101_021718dd.csv' 双吸引子 '20000101_021921ss.csv' 单吸引子   '20000101_022112tr.csv' 三周期
# '20000101_022321zhenfa.csv' 阵发混沌
# '20000101_022614f.csv' 四周期    '20000101_022700d.csv' 双周期   '20000101_022739s.csv' 单周期
CH2_raw = pd.read_csv(filename,sep=',',header=9,usecols=[2])
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

plt.plot(t[:loc],power2[:loc])
plt.xlabel('Frequency')
plt.ylabel('Power')
plt.title('U2 Power Spectrum')
plt.show()
