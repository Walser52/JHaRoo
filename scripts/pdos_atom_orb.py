import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from QEplots import reader, prepareDOS, plotDOS


#================= DOS=======================
title = 'CsPbI3'
pdos_folder = r'../data/pdos_files/7_PDOS'
totaldosfile = 'aiida.pdos_tot'
saveto = '../plots/DFT_PDOS_atom_orb'
toskip = {'Cs': ['s', 'p', 'd'], 'Pb': ['d'], 'Br':[]}

efermi = 3.6711


#___________plotsettings
xrange = [0,3]
yrange = [-4,10]

plotTDOS = True
#===============================================


if __name__ == '__main__':


  all_pdos = reader(pdos_folder, contains = 'pdos')

  pdos_data, energy_tot, dos_tot = prepareDOS(all_pdos, pdos_folder, totaldosfile, toskip, plotTotal = plotTDOS)
  plotDOS(pdos_data, energy_tot, dos_tot, efermi, xrange, yrange, title, saveto, plotTDOS = plotTDOS)



  print(pdos_data['Pb-p'])

#  plt.show()
  
