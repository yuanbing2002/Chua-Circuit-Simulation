import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import pandas as pd

# constants
global C1, C2, L, R,G
C1 = 11.0381e-9 # F
C2 = 100.674e-9 # F
L = 27e-3 # H
R_start = 1875
R_end = 1905
dR = 0.01

# initial condition
t0 = 0
y0 = np.array([0.0,0.0,0.001]) # [U1, U2, I]
t_final = 0.2
t_total = 10000

# I-V curve of the nonlinear negative resistance
def g(U):
    Ga = -0.00076 # omega^(-1) uncertainty: 0.1*10^(-4)
    Gb = -0.00049 # omega^(-1) uncertainty: 0.06*10^(-4)
    E = 15.0 #V
    g = Gb*U+(Gb-Ga)/2*(abs(U-E)-abs(U+E))
    return g

# chua's circuit
def f(y,t):
    y1 = (G*(y[1]-y[0])-g(y[0]))/C1
    y2 = (G*(y[0]-y[1])+y[2])/C2
    y3 = -y[1]/L
    return np.array([y1, y2, y3])

# find local minimum function
def mini(data):
    '''input the data list'''
    length = len(data)
    ans = []
    for i in range(2,length-2):
        if data[i]<data[i-1] and data[i]<data[i-2] and data[i]<data[i+1] and data[i]<data[i+2]:
            ans.append(data[i])
    return ans

time=np.linspace(t0,t_final,t_total)
R_list = [R_start + i*dR for i in range(int((R_end-R_start)/dR))]
R1list = [] # for bifurcation diagram
R2list = []
U1min = [] # also for bifurcation diagram
U2min = []
for R in R_list:
    G = 1/R
    y = odeint(f,y0,time)
    '''
    # phase plot
    plt.plot(y[1000:,0],y[1000:,1] , label = R )
    plt.xlabel('U1')
    plt.ylabel('U2')
    plt.legend()
    plt.savefig('%f omega.jpg'%round(R,1))
    plt.clf()
    print('%f omega Done!'%round(R,1))
    

    # simulation data plot
    plt.plot(time[1000:2000:],y[1000:2000,0],label = 'U1')
    plt.plot(time[1000:2000:], y[1000:2000,1], label='U2')
    plt.xlabel('t')
    plt.ylabel('U')
    plt.title('R = %f omega'% round(R, 1))
    plt.legend()
    plt.savefig('%f omega.jpg' % round(R, 1))
    plt.clf()
    print('%f omega Done!' % round(R, 1))

    # output simulating data
    dataframe = pd.DataFrame({'t': time[1000::].tolist(), 'U1': y[1000:,0].tolist()})
    dataframe.to_csv("%f omega.csv"%round(R,1), index=False, sep=',')
    '''

    # find the local minimum
    y1list= y[1000:,0].tolist()
    U1min += mini(y1list)
    R1list += [R+i-i for i in range(len(mini(y1list)))]
    y2list = y[1000:, 1].tolist()
    U2min += mini(y2list)
    R2list += [R + i - i for i in range(len(mini(y2list)))]
    print('R = %f omega'%round(R,3))
print(len(R2list))
print(len(U2min))
plt.scatter(R1list,U1min,s=0.1,alpha = 1)
plt.xlabel('R/omega')
plt.ylabel('U1min')
plt.title('Bifurcation Diagram for U1min')
plt.savefig('U1min')
plt.clf()

plt.scatter(R2list,U2min,s=0.1,alpha = 1)
plt.xlabel('R/omega')
plt.ylabel('U2min')
plt.title('Bifurcation Diagram for U2min')
plt.savefig('U2min')
plt.clf()

dataframe1 = pd.DataFrame({'R': R1list, 'U1min': U1min})
dataframe1.to_csv("U1min.csv", index=False, sep=',')
dataframe2 = pd.DataFrame({'R': R2list, 'U1min': U2min})
dataframe2.to_csv("U2min.csv", index=False, sep=',')