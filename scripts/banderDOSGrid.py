import matplotlib.pyplot as plt
import numpy as np
import os
import glob

from jhr.plotters.express import DOSExpress
from jhr.plotters.express import bandsExpress

from jhr.plotters._base import createTag, annotate, ax_divider
from matplotlib.gridspec import GridSpec

from cycler import cycler

# from materials.CsPbBr3_info import *
# from materials.CsPbI3_info import *
# from materials.CsPbBr2I_info import *
# from materials.CsPbBrI2_info import *



showplot = False

mats = ['CsPbBr3_info', 'CsPbI3_info', 'CsPbBr2I_info', 'CsPbBrI2_info' ]
mats = ['materials/' + m + '.py' for m in mats]

fig, Axs =  plt.subplots(2, 2, figsize=(12, 10))  
title = 'grid'

plt.subplots_adjust(left=0.05,
                    bottom=0.05, 
                    right=0.95, 
                    top=0.95, 
                    wspace=0.2, 
                    hspace=0.3)

#======================================================

if len(Axs) > 1: Axs = Axs.flatten()
else: Axs = [Axs]


#________Data settings___________

savefile = f'../plots/Grids/{title}'
DOS_cycler = cycler(color=['#003049', '#f77f00', '#B028C6', '#f2542d', '#562c2c'])

high_symmetry_points = {#Define High Symmetry Points
    '$\Gamma$'   : 0,
    'X'          : 30,
    'M'          : 60,
    '$\Gamma$ '  : 90,
    'R'          : 120,
    'X|M'        : 150,
    'R '         : 180
}



for m, ax in zip(mats, Axs):
  print(m)
  with open(m) as f:
    exec(f.read())

  #_________Plot settings__________
  #DOS Plot settings
  plotsettingsDOS = {
      'plot':{'x':[], 'y': [], 'label': [], 'alpha': 1, 'lw':0.9}, 
      'xlabel': 'DOS (states/eV)', 
      'set_prop_cycle': DOS_cycler,
      'xlim': xlimDOS,      
      'ylim': ylimDOS,
      'legend': {'frameon': False, 'ncol':2, 'fontsize': 9}}

  #Bands Plot settings
  plotsettingsBands = {
      'plot':{'x':[], 'y': [], 'alpha': 0.8, 'color': '#1C829C', 'lw': 0.9}, 
      'yaxis.set_minor_locator': {'AutoMinorLocator': 2},
      'xlabel': 'k points', 
      'ylabel': 'Energy (eV)',
      'ylim': ylimBands,
      'legend': {'frameon': False, },
  }

  plotsettingsW90Bands = {
      'plot':{'x':[], 'y': [], 'alpha': 0.8, 'color': 'green'}, 
  }

  #Create dictionary
  mat = {'DOS': dict(pdos_folder = pdos_folder, totaldosfile = totaldosfile, 
                    toskip = toskipDOS, efermi = efermi, plotTDOS = plotTDOS, plotsettings = plotsettingsDOS),

        'bands': dict(data_file = bandsQEFile, plotsettings = plotsettingsBands, toskip = toskipbands, code = 'QE',
                      symmPoints = high_symmetry_points , efermi = efermi, 
                      showhomolumo = showhomolumo, homolumosettings = {'fontsize': 8}
                      
                      ),

        'w90bands': dict(data_file = (dat_file_wann, gnu_file_wann), plotsettings= plotsettingsW90Bands, efermi = efermi, toskip = [], code = 'W90')
  }

  plt.sca(ax)
  ax1, ax2 = ax_divider(ax, divisions = 2, direction = "right", pad = 0.2, share = False)

  plt.sca(ax1)
  bandsExpress(**mat['bands'])
  createTag(name = plottag, pos = (0.02, 1.02), weight = 'bold', fontcolor = '#003030' ,  bboxsettings = dict(alpha = 0))
  plt.sca(ax2)
  DOSExpress(**mat['DOS'])
  ax2.set_yticklabels([])


annotate(labels = 'abcd    ',append = '')
plt.savefig(savefile+'.png', format = 'png', dpi = 350, transparent = True)
plt.savefig(savefile+'.svg', format = 'svg', transparent = True)

if showplot: plt.show()


#============PLOTTER==============

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 8), sharey = True)  # 2 rows, 1 column

# plt.sca(ax2)
# DOSExpress(**mat['DOS'])

# plt.sca(ax1)
# bandsExpress(**mat['bands'])
# #bandsExpress(**mat['w90bands'])

# createTag(name = title, pos = (0.02, .95), weight = 'bold', fontcolor = '#555555' ,  bboxsettings = dict(alpha = 0))
# #annotate(append = '.')

# fig.tight_layout()
# plt.subplots_adjust(wspace=0.04, hspace=0)

# plt.savefig(savefile+'.png', format = 'png', dpi = 350, transparent = True)
# plt.savefig(savefile+'.svg', format = 'svg', transparent = True)

# if showplot: plt.show()

  
#========================================


# plt.show()