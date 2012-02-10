import avalanchetoolbox
import powerlaw
from scipy.io import loadmat
from numpy import concatenate, array
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

files = [#'read_rep12t_tr1', 'read_rep12t_tr2',\
#        'VGdt12_tr1', 'VGdt12_tr2',\
#        'VGOP12t_tr1', 
        'VGOP12t_tr2']

for file in files:
    print('Constructing data from '+file)
    plots = PdfPages('/data/alstottj/Yamagata/Figures/2012-2-9/'+file+'.pdf')
    mat = loadmat('/data/alstottj/Yamagata/p7_YA/'+file+'.mat')
    if 'C' in mat.keys():
        data_key = 'C'
    else:
        data_key = 'A'
    d = mat[data_key][:64,:,1]
    d_all = d
    for i in range(64):
        d_all = concatenate((d_all, mat[data_key][:64,:,i+1]),1)

    print('Analyzing single channel')
    avalanchetoolbox.avalanches.signal_variability(d_all[33,:],)
    pyplot.xlabel('Signal range (Standard deviation)')
    pyplot.ylabel('Range probability (log(p))')
    plots.savefig()
    pyplot.close('all')

    print('Analyzing all channels')
    active_sensors = avalanchetoolbox.avalanches.signal_variability(d_all, (8,8))
    plots.savefig()
    pyplot.close('all')


    print('Running avalanche analyses')
    avs = array([])
    for i in range(80):
        d = mat[data_key][:64,:,i]
        m = avalanchetoolbox.avalanches.run_analysis(d, time_scale='mean_iei', threshold_mode='Likelihood', threshold_level=10)
        if 'size_events' in m.keys():
            avs = concatenate((avs, m['size_events']), 1)

    pyplot.figure()
    powerlaw.plot_cdf(avs)
    pyplot.xlim(1,100)
    pyplot.plot((active_sensors, active_sensors), pyplot.ylim())
    pyplot.title('Neuronal avalanche size distribution, survival function')
    pyplot.xlabel('Avalanche Size (number of events)')
    pyplot.ylabel('P(Size>x)')
    plots.savefig()
    pyplot.close('all')
    plots.close()
