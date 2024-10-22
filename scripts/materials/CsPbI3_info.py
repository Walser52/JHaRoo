# Sample data file for bandsDOSW90.py

title = 'CsPbI3'
efermi = 3.6711
plottag = '$CsPbI_{3}$'

#DOS Data
pdos_folder = r'../data/pdos_files/CsPBI3_PDOS'
totaldosfile = 'aiida.pdos_tot'
toskipDOS =  {'Cs': ['s', 'p', 'd'], 'Pb': ['d'], 'Br':['s'], 'I':['s']}
plotTDOS = True

xlimDOS = [0,10]
ylimDOS = [-4,10]

#Bands Data
bandsQEFile = '../data/band_files/CsPbI3.bands.gnu'
toskipbands = list(range(0, 12)) + []
#xlimBands = []      
ylimBands = ylimDOS

#W90 Bands Data
dat_file_wann = '../data/wann_band_files/CsPBI3_band_wann.dat'
gnu_file_wann = '../data/wann_band_files/CsPBI3_band_wann.gnu'


showhomolumo = 4
