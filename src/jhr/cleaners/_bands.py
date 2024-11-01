import numpy as np

def _findBandgap(bands, printall = False, sort = False, threshold = 0.1, window = [], index = []):
  """
  Takes a 2D numpy array of bands  and returns the bandgaps and the values at which that gap occurs.
  Args:
    bands: 2D array of bands. First index is band number (n), second index is band values at different k. 
    printall: If True prints all bandgaps
    sort: If the bands are unsorted and need sorting.
    threshold: Only gaps greater than threshold are considered. 
    index: Only keeps the bands that lie between the index limits. 
    window: Only keeps the bands that overlap with the window provided. 

  Note:
    Both index and window cannot be given simulatneously
  """

  #_________Find minima and maxima of each band_________
  bandminmax = []
  for band in bands:
    bandminmax.append([band.min(), band.max(), np.argmin(band), np.argmax(band)])
    
  bandsxy = np.array(bandminmax)
 

  #_________Find which bands to drop________________
  if (len(index) > 0) and (len(window) > 0):
    raise ValueError("Error: Both index and window cannot be given at the same time.")

  if len(index) > 0: 
    bandsxy = bandsxy[index[0]:index[1], :]
  
  if len(window) > 0: 
    mask = (bandsxy[:, 0] <= window[1]) & (bandsxy[:, 1] >= window[0])
    bandsxy = bandsxy[mask]



  if sort: 
    bandsxy = bandsxy[bandsxy[:, 0].argsort()]


  #___________Find overlap__________

  bandgaps = bandsxy[1:, 0]  - bandsxy[:-1, 1] 
  where = np.where(bandgaps > threshold)[0]
  bandgaps = bandgaps[bandgaps > threshold]




  homolumo = []
  for i in where:
    row = [bandsxy[i,1], bandsxy[i+1,0], bandsxy[i,3], bandsxy[i+1,2]]
    homolumo.append(row)

  if printall is True: 
    print("Lumo (eV), Homo (eV), Lumo (k), Homo(k) \n")
    print(homolumo)
    print("-------------")
    print("Bandgaps")
    print(bandgaps)

  

  return np.array(homolumo), bandgaps



