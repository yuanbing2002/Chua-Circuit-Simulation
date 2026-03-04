import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import pandas as pd

# constants
global C1, C2, L, R,G
C1 = 11.0381e-9 # F
C2 = 100.674e-9 # F
L = 27e-3 # H
R_start = 1860
R_end = 1905
dR = 0.1

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

time=np.linspace(t0,t_final,t_total)
R_list = [R_start + i*dR for i in range(int((R_end-R_start)/dR))]
R1list = [] # for bifurcation diagram
R2list = []
U1min = [] # also for bifurcation diagram
U2min = []
for R in R_list:
    G = 1/R
    y = odeint(f,y0,time)

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