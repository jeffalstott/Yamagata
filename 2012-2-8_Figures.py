import avalanchetoolbox
import powerlaw
from scipy.io import loadmat
from numpy import concatenate, array
from matplotlib import pyplot

mat = loadmat('/data/alstottj/Yamagata/p7_YA/read_rep12t_tr1.mat')

d = mat['C'][:64,:,1]
d_all = d
for i in range(64):
    d_all = concatenate((d_all, mat['C'][:64,:,i+1]),1)

avalanchetoolbox.avalanches.signal_variability(d_all[33,:],)
pyplot.xlabel('Signal range (Standard deviation)')
pyplot.ylabel('Range probability (log(p))')

avalanchetoolbox.avalanches.signal_variability(d_all, (8,8))
pyplot.xlabel('Signal range (Standard deviation)')
pyplot.ylabel('Range probability (log(p))')

avs = array([])

for i in range(80):
    d = mat['C'][:64,:,i]
    m = avalanchetoolbox.avalanches.run_analysis(d, time_scale='mean_iei', threshold_mode='Likelihood', threshold_level=10)
    avs = concatenate((avs, m['size_events']), 1)

pyplot.figure()
powerlaw.plot_cdf(avs)
pyplot.title('Neuronal avalanche size distribution, survival function')
pyplot.xlabel('Avalanche Size (number of events)')
pyplot.ylabel('P(Size>x)')
