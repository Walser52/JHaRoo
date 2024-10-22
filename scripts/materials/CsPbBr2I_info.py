# Sample data file for bandsDOSW90.py

title = 'CsPbBr2I'
plottag = '$CsPbBr_{2}I$'
efermi =3.1106

#DOS Data
pdos_folder = r'../data/pdos_files/CsPBBr2I_PDOS'
totaldosfile = 'aiida.pdos_tot'
toskipDOS = {'Cs': ['s', 'p', 'd'], 'Pb': ['d'], 'Br':['s'], 'I':['s']}
plotTDOS = True

xlimDOS = [0,5]
ylimDOS = [-6,10]

#Bands Data
bandsQEFile = '../data/band_files/CsPbBr2I.bands.gnu'
toskipbands = list(range(0, 12)) + []
#xlimBands = []      
ylimBands = ylimDOS

#W90 Bands Data
dat_file_wann = '../data/wann_band_files/CsPbBr2I_band_wann.dat'
gnu_file_wann = '../data/wann_band_files/CsPbBr2I_band_wann.gnu'


showhomolumo = 5