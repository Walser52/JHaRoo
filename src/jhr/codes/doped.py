import os
import pandas as pd

class Doped():
  """
  Routines for the doped code.
  """

  # Define a function to collect file paths
  @staticmethod
  def collect_file_paths(root_dir):
      """
      Return dataframe of VASP files made by doped. Uses subfolders as multilevel index.
      """
      # Initialize lists to store the data
      folder_paths = []
      subfolder_paths = []
      incar_paths = []
      poscar_paths = []
      kpoints_paths = []
      
      # Traverse through the root directory
      for folder_name in os.listdir(root_dir):
          folder_path = os.path.join(root_dir, folder_name)
          if os.path.isdir(folder_path):
              for subfolder_name in os.listdir(folder_path):
                  subfolder_path = os.path.join(folder_path, subfolder_name)
                  if os.path.isdir(subfolder_path):
                      # Collect file paths inside the subfolder
                      incar = os.path.join(subfolder_path, 'INCAR')
                      poscar = os.path.join(subfolder_path, 'POSCAR')
                      kpoints = os.path.join(subfolder_path, 'KPOINTS')
                      
                      # Append data to the lists
                      folder_paths.append(folder_name)
                      subfolder_paths.append(subfolder_name)
                      incar_paths.append(incar if os.path.exists(incar) else None)
                      poscar_paths.append(poscar if os.path.exists(poscar) else None)
                      kpoints_paths.append(kpoints if os.path.exists(kpoints) else None)

      # Create a DataFrame with multi-level index
      data = {
          'INCAR': incar_paths,
          'POSCAR': poscar_paths,
          'KPOINTS': kpoints_paths
      }
      df = pd.DataFrame(data, index=[folder_paths, subfolder_paths])
      
      return df

