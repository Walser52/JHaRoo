# Sample data file for bandsDOSW90.py

title = 'CsPbBr3'
plottag = '$CsPbBr_{3}$'

efermi = 3.6711

#DOS Data
pdos_folder = r'../data/pdos_files/CsPBBr3_PDOS'
totaldosfile = 'aiida.pdos_tot'
toskipDOS = {'Cs': ['s', 'p', 'd'], 'Pb': ['d'], 'Br':['s'], 'I':['s']}
plotTDOS = True

xlimDOS = [0,10]
ylimDOS = [-6,8.5]

#Bands Data
bandsQEFile = '../data/band_files/CsPbBr3.bands.gnu'
toskipbands = list(range(0, 12)) + []
#xlimBands = []      
ylimBands = ylimDOS

#W90 Bands Data
dat_file_wann = '../data/wann_band_files/CsPBBr3_band_wann.dat'
gnu_file_wann = '../data/wann_band_files/CsPBBr3_band_wann.gnu'

showhomolumo = 4


