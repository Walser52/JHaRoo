from jhr.cleaners.bands import bandhandler
from jhr.cleaners.DOS import DOShandler

from jhr.plotters.plots import plotBands
from jhr.plotters.plots import plotDOS

from jhr.cleaners.wannier import wannbandhandler
from jhr.plotters.plots import plotwannbands

#____________Express functions_____________

def bandsExpress(data_file, high_symmetry_points, efermi, toskip, settings, code='QE'):
  """
  High level, one line function to plot bands quickly. 

  Args:

    settings: Settings for plot
  """

  #_____________Process Data_____________
  if code == 'QE':
    k, bands, positions, labels, (homo, lumo), bandgap = bandhandler(data_file, high_symmetry_points, efermi)
  if code == 'W90':
    pass

  #_______________PLOT___________________
  
  settings['plot']['x'] = k
  settings['plot']['y'] = bands.T
  settings['xlim'] = [min(positions), max(positions)]
  settings['xticks'] = {'ticks': positions, 'labels':  labels}

  plotBands(high_symmetry_points, settings, toskip = toskip, efermi = efermi)


  return

#_______________________________DOS_________________________________
def DOSExpress(pdos_folder, totaldosfile, toskip, plotTDOS, efermi, settings):

  x,y,labels = DOShandler(pdos_folder, totaldosfile, toskip, plotTDOS, efermi)

  settings['plot']['x'] = x
  settings['plot']['y'] = y
  settings['plot']['label'] = labels

  plotDOS(settings)
  return
#_______________________________________WannBands_____________________
def wannbandsExpress(dat_file_wann, gnu_file_wann, efermi, settings):
    
  k_points, bands, high_symmetry_points, other_settings, positions, labels, (homo, lumo), bandgap = wannbandhandler(dat_file_wann, gnu_file_wann, efermi)
  settings['plot']['x'] = k_points
  settings['plot']['y'] = bands.T
  settings['xlim'] = [min(positions), max(positions)]
  settings['xticks'] = {'ticks': positions, 'labels':  labels}

# plotBands(high_symmetry_points, settings, toskip = toskip, efermi = efermi)

  plotwannbands(settings, efermi)
  return
