##RICORDA CHE PER PLOTTARE VA MESSO IN noVNC!

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
X1=raw.get_data(picks=picks)
picks=[raw.ch_names.index('Cz..')]
X2=raw.get_data(picks=picks)
picks=[raw.ch_names.index('C4..')]
X3=raw.get_data(picks=picks)

np.savetxt('X1.dat', X1, delimiter='\n')
np.savetxt('X2.dat', X2, delimiter='\n')
np.savetxt('X3.dat', X3, delimiter='\n')

fs = 160