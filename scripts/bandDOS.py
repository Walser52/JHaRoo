import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from QEplots import readfolder, allDOS, plotDOS


#================= DOS=======================
title = 'CsPbBr3'
pdos_folder = r'../data/pdos_files/CsPBBr3_PDOS'
totaldosfile = 'aiida.pdos_tot'
saveto = '../plots/DFT_PDOS_atom_orb'
toskip = {'Cs': ['s', 'p', 'd'], 'Pb': ['d'], 'Br':[]}

efermi = 1.9671


#___________plotsettings
xrange = [0,3]
yrange = [-4,10]

plotTDOS = False
#===============================================

if __name__ == '__main__':

  # Consolidate DOS DATA
  all_pdos = readfolder(pdos_folder, contains = 'pdos')
  pdos_data, energy_tot, dos_tot = allDOS(all_pdos, pdos_folder, totaldosfile, toskip, plotTotal = plotTDOS)

  #Consolidate Bands DATA
  
  #Plot DOS
  plotDOS(pdos_data, energy_tot, dos_tot, efermi, xrange, yrange, title, saveto, plotTDOS = plotTDOS)

  #Plot Bands



#  plt.show()
  
