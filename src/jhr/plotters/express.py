from jhr.cleaners.bandsQE import bandHandlerQE
from jhr.cleaners.bandsW90 import bandHandlerW90

from jhr.cleaners.DOSQE import DOSHandlerQE

from jhr.plotters.plots import plotBands
from jhr.plotters.plots import plotDOS

import os


#____________Express functions_____________

def bandsExpress(data_file, plotsettings, toskip = [], code='QE', **kwargs):
  """
  High level, one line function to plot bands quickly. 

  Args:

    settings: Settings for plot
    data_file: 
              For QE: Single file containing the data.
              For W90: Tuple of files. (wannier .dat data_file, wannier gnu_file)

    kwargs: 
      symmPoints = 'Dictionary of high symmetry points'
      efermi = Float indicating fermi energy level.
  """



  if 'symmPoints' in kwargs.keys(): high_symmetry_points = kwargs['symmPoints']
  if 'efermi' in kwargs.keys(): efermi = kwargs['efermi'] 
  else: efermi = 0

  #_____________Process Data_____________
  if code.lower() == 'qe':
    k, bands, positions, labels, (homo, lumo), bandgap = bandHandlerQE(data_file, high_symmetry_points, efermi)

  if code.lower() == 'w90':
    if len(data_file) == 2:
      for f in data_file:
          if os.path.splitext(f)[1] == '.gnu':
              gnu_file_wann = f
          elif os.path.splitext(f)[1] == '.dat':
              data_file_wann = f

      k, bands, high_symmetry_points, other_settings, positions, labels, (homo, lumo), bandgap = bandHandlerW90(data_file_wann, gnu_file_wann, efermi)


  #_______________PLOT___________________
  
  plotsettings['plot']['x'] = k
  plotsettings['plot']['y'] = bands.T
  plotsettings['xlim'] = [min(positions), max(positions)]
  plotsettings['xticks'] = {'ticks': positions, 'labels':  labels}


  plotBands(high_symmetry_points, plotsettings, toskip = toskip, efermi = efermi)

  return





#_______________________________DOS_________________________________
def DOSExpress(pdos_folder, totaldosfile, toskip, plotTDOS, efermi, plotsettings):

  x,y,labels = DOSHandlerQE(pdos_folder, totaldosfile, toskip, plotTDOS, efermi)

  plotsettings['plot']['x'] = x
  plotsettings['plot']['y'] = y
  plotsettings['plot']['label'] = labels

  plotDOS(plotsettings)
  return


