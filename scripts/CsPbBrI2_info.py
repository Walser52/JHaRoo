# Sample data file for bandsDOSW90.py

title = 'CsPbBrI2'
efermi = 5.7132

#DOS Data
pdos_folder = r'../data/pdos_files/CsPBBrI2_PDOS'
totaldosfile = 'aiida.pdos_tot'
toskipDOS = {'Cs': [], 'Pb': ['d'], 'Br':['s'], 'I':['s']}
plotTDOS = True

xlimDOS = [0,10]
ylimDOS = [-4,10]

#Bands Data
bandsQEFile = '../data/band_files/CsPbBrI2.bands.gnu'
toskipbands = list(range(0, 12)) + []
#xlimBands = []      
ylimBands = [-6,10]

#W90 Bands Data
dat_file_wann = '../data/wann_band_files/CsPBBrI2_band_wann.dat'
gnu_file_wann = '../data/wann_band_files/CsPBBrI2_band_wann.gnu'



