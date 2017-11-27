# -*- coding: utf-8 -*-
"""
Esperimento - clustering nello spazio di Riemann

Luca Talevi (talevi.luca@gmail.com)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci #motor imagery dataset
from mne.filter import filter_data
#reference: http://www.martinos.org/mne/stable/generated/mne.datasets.eegbci.load_data.html

subject=1
runs=[3, 7, 11] #motor execution

raw_fnames = eegbci.load_data(subject, runs) #contiene i file edf
raws = [read_raw_edf(f, preload=True) for f in raw_fnames] #memorizza in raws i contenuti dei file edf
raw = concatenate_raws(raws) #concatena i contenuti dei file edf in un solo raw

raw.drop_channels(['STI 014'])

picks=[raw.ch_names.index('C3..')]
picks.append(raw.ch_names.index('Cz..'))
picks.append(raw.ch_names.index('C4..'))

print(picks)

X=raw.get_data(picks=picks) #i tre segnali di interesse

print(X.shape)

fs=160 #estratto dalle info del raw

#voglio una finestra in grado di cogliere tra gli 8 e i 30 Hz, quindi devo prendere una lunghezza 160/8
wlen=int(np.ceil(fs/8))
filter_data(X, fs, 8, 30) #filtraggio 8-30

cov_c3cz=list()
cov_c3c4=list()
cov_czc4=list()

for i in range(wlen,max(X.shape)):
    cov_c3cz.append(np.cov(X[[0,1],i-wlen:i]))
    cov_c3c4.append(np.cov(X[[0,2],i-wlen:i]))
    cov_czc4.append(np.cov(X[[1,2],i-wlen:i]))

print(wlen)
print(len(cov_c3cz))
print(cov_c3cz[0])

x_c3cz=np.zeros([3,len(cov_c3cz)])
x_c3c4=np.zeros([3,len(cov_c3cz)])
x_czc4=np.zeros([3,len(cov_c3cz)])

for i in range(len(cov_c3cz)):
    x_c3cz[0,i]=cov_c3cz[i][0,0] #var c3
    x_c3cz[1,i]=cov_c3cz[i][1,1] #var cz
    x_c3cz[2,i]=cov_c3cz[i][0,1] #covar c3cz

    x_c3c4[0,i]=cov_c3c4[i][0,0] #var c3
    x_c3c4[1,i]=cov_c3c4[i][1,1] #var c4
    x_c3c4[2,i]=cov_c3c4[i][0,1] #covar c3c4

    x_czc4[0,i]=cov_czc4[i][0,0] #var cz
    x_czc4[1,i]=cov_czc4[i][1,1] #var c4
    x_czc4[2,i]=cov_czc4[i][0,1] #covar czc4


fig = plt.figure()

#####################################################

##GRAFICI SINGOLI

# ax1 = fig.add_subplot(131, projection='3d')
# ax2 = fig.add_subplot(132, projection='3d')
# ax3 = fig.add_subplot(133, projection='3d')

# ax1.plot(x_c3cz[0,:],x_c3cz[1,:],x_c3cz[2,:])
# ax1.set_xlabel('var c3')
# ax1.set_ylabel('var cz')
# ax1.set_zlabel('covar c3cz')

# ax2.plot(x_c3c4[0,:],x_c3c4[1,:],x_c3c4[2,:])
# ax2.set_xlabel('var c3')
# ax2.set_ylabel('var c4')
# ax2.set_zlabel('covar c3c4')

# ax3.plot(x_czc4[0,:],x_czc4[1,:],x_czc4[2,:])
# ax3.set_xlabel('var cz')
# ax3.set_ylabel('var c4')
# ax3.set_zlabel('covar czc4')

#####################################################

##GRAFICO COMPLESSIVO

# ax = fig.add_subplot(111, projection='3d')

# ax.plot(x_c3cz[0,:],x_c3cz[1,:],x_c3cz[2,:],'r')
# ax.plot(x_c3c4[0,:],x_c3c4[1,:],x_c3c4[2,:],'g')
# ax.plot(x_czc4[0,:],x_czc4[1,:],x_czc4[2,:],'b')
# ax.legend(['c3cz','c3c4','czc4'])

# plt.show()

#####################################################

## ANIMAZIONE

ax = fig.add_subplot(111, projection='3d')

ax.set_xlim3d( [ min([min(x_c3cz[0,:]),min(x_c3c4[0,:]),min(x_czc4[0,:])]) , max([max(x_c3cz[0,:]),max(x_c3c4[0,:]),max(x_czc4[0,:])]) ] )
ax.set_ylim3d( [ min([min(x_c3cz[1,:]),min(x_c3c4[1,:]),min(x_czc4[1,:])]) , max([max(x_c3cz[1,:]),max(x_c3c4[1,:]),max(x_czc4[1,:])]) ] )
ax.set_zlim3d( [ min([min(x_c3cz[2,:]),min(x_c3c4[2,:]),min(x_czc4[2,:])]) , max([max(x_c3cz[2,:]),max(x_c3c4[2,:]),max(x_czc4[2,:])]) ] )

NUM=4

for i in range(NUM,x_c3cz.size):
    if i==NUM:
        p1, = ax.plot(x_c3cz[0,:i],x_c3cz[1,:i],x_c3cz[2,:i],'r')
        p2, = ax.plot(x_c3c4[0,:i],x_c3c4[1,:i],x_c3c4[2,:i],'g')
        p3, = ax.plot(x_czc4[0,:i],x_czc4[1,:i],x_czc4[2,:i],'b')
    else:
        x1=x_c3cz[0,:i]
        y1=x_c3cz[1,:i]
        z1=x_c3cz[2,:i]
        p1.set_data(x1,y1)
        p1.set_3d_properties(z1)

        x2=x_c3c4[0,:i]
        y2=x_c3c4[1,:i]
        z2=x_c3c4[2,:i]
        p2.set_data(x2,y2)
        p2.set_3d_properties(z2)

        x3=x_czc4[0,:i]
        y3=x_czc4[1,:i]
        z3=x_czc4[2,:i]
        p3.set_data(x3,y3)
        p3.set_3d_properties(z3)

    plt.pause(1/(4*fs))
