import matplotlib.pyplot as plt
from cycler import cycler
import os
import numpy as np
from jhr.plotters._base import makeplot




#_____________Mid level plotting functions______________

def plotBands(symmpoints, settings, toskip = [], efermi = None):
  """
  Plots bands

  Args:

  """

  if efermi is not None:
     settings['plot']['y'] -= efermi

  if len(toskip) > 0:
    settings['plot']['y'] = np.delete(settings['plot']['y'], toskip, 1)

  makeplot(plt.plot, settings)  

  return 


def plotDOS(settings):
  #_________________PLOT________________________


  makeplot(plt.plot, settings)



  return


def plot(what = 'Bands'):
  return 




#____________________wannBands_______________________
def plotwannbands(settings, efermi):
  if efermi is not None:
     settings['plot']['y'] -= efermi

  # for band in range(len(bands)):
  #       plt.plot(k_points, bands[band, :] - efermi)
  makeplot(plt.plot, settings)

  return
