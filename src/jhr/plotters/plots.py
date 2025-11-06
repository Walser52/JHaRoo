import matplotlib.pyplot as plt
from cycler import cycler
import os
import numpy as np
from jhr.plotters._base import makeplot, arrowDouble

from matplotlib import ticker

from jhr._helpers import trunc

#_____________Mid level plotting functions______________

def plotBands(settings, toskip = [], efermi = None):
  """
  Plots bands

  Args:

  """

  if efermi is not None:
     settings['plot']['y'] -= efermi

  if len(toskip) > 0:
    settings['plot']['y'] = np.delete(settings['plot']['y'], toskip, 1)

  makeplot(plt.plot, settings)  


  kpoints = settings['plot']['x']

  for sp in settings['xticks']['ticks']:
    plt.axvline(sp, ls = '--', dashes=(5, 5),color = '#CCCCCC', zorder = 1)

  return 


def plotDOS(settings):
  #_________________PLOT________________________


  makeplot(plt.plot, settings)



  return


def plotHomoLumo(homolumo, show = None, efermi = None, linesettings = None, textsettings = None, annotate = True):
  """
  Plots homo-lumo lines.
  Args:
    homolumo: list of values at which to plot. 
    show: 
        - list e.g. [1,2]. Plot both 1 and 2 indices. 
        - int e.g. 2. Plot lines for bandgap 2 only. 
        - 'all'. Draw lines for all. 
    annotate:     Whether to add bandgap text and double headed arrows to plot. True by default.
    linesettings: Settings for horizontal lines. Passed to plt.plot
    textsettings: Settings for bandgap text. Passed to plt.text
  """


  if efermi is not None: 
    homolumo[:, 0] = homolumo[:, 0] - efermi
    homolumo[:, 1] = homolumo[:, 1] - efermi


  if type(show) is int: show = [show]
  if show == 'all': show = range(len(homolumo))

  if linesettings is None: linesettings = {'c': 'k', 'lw': 0.8, 'ls':'--'}

  #__Settings for printing bandgap___
  bandgaps = homolumo[:, 1] - homolumo[:, 0]
  textsettings_def = {'fontsize': '10', 'ha': 'center', 'va': 'center'}
  if textsettings is not None: textsettings_def.update(textsettings)



  #___Show bandgaps____
  if show is not None:
    for i in show:
      #____Create horizontal lines_____      
      ly, hy, lx, hx = homolumo[i]
      #____Add text showing bandgap with arrows____    
      if annotate: 
        bg = trunc(bandgaps[i],2)
        arrowDouble(xyfrom = [lx,ly], xyto = [hx, hy], xytext = None, text = f"{bg} eV", textsettings = textsettings)


      plt.plot([lx-0.5, lx+0.5], [ly, ly], **linesettings)
      plt.plot([hx-0.5, hx+0.5], [hy, hy], **linesettings)


  return 



#____________________wannBands_______________________
def plotwannbands(settings, efermi):
  if efermi is not None:
     settings['plot']['y'] -= efermi

  # for band in range(len(bands)):
  #       plt.plot(k_points, bands[band, :] - efermi)
  makeplot(plt.plot, settings)

  return


#________________Heat Maps_____________
def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", ticks = True, **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current Axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    if not ticks:
      ax.set_xticks([])
      ax.set_yticks([])



    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

def tbHeat(H, num_basis = 12, ax = None, cbar_kw = None, ticks = True ):
  """
  Plot a tight binding heat map.
  """

  rows = list(range(1,num_basis + 1))
  cols = list(range(1,num_basis + 1))

  im, cbar = heatmap(H, rows, cols, ax=ax,
                    cmap="YlGn", 
                    #  cmap="Blues_r", 
                    cbarlabel="Log of Absolute Hopping strength",
                    cbar_kw = cbar_kw, 
                    ticks = ticks)
  texts = annotate_heatmap(im, valfmt="{x:.2f}")
  return
